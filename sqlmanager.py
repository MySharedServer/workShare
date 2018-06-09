from .base import *


class SqlManager():

    day_sql = """
        SELECT case when t4.talk_sum is null then 0 else t4.talk_sum end as talk_sum,
              case when t4.steps_sum is null then 0 else t4.steps_sum end as steps_sum 
        FROM 
        ( 
            SELECT * 
            FROM 
            (
                VALUES(extract(year from to_date(%s, 'YYYY-MM-DD HH24-MI-SS')),
                extract(month from to_date(%s, 'YYYY-MM-DD HH24-MI-SS')),
                extract(day from to_date(%s, 'YYYY-MM-DD HH24-MI-SS')))
            ) as t3_1 (cur_year, cur_month,cur_day),
                (VALUES(0),(1),(2),(3),(4),(5),(6),(7),(8),(9),(10),(11),(12),(13),(14),(15),(16),(17),(18),(19),(20),(21),(22),(23)) as t3_2 (cur_hour),
                (VALUES(0),(1),(2),(3),(4),(5),(6),(7),(8),(9),(10),(11)) as t3_3 (minutes_group)
        ) t3
        LEFT JOIN
        (
            SELECT t2.years,t2.months,t2.days,t2.hours, t2.minutes_group,
                    sum(t2.talk) as talk_sum, sum(t2.steps) as steps_sum
            FROM
            (
                SELECT
                    extract(year from to_timestamp(t1.timestamp)) as years, extract(month from to_timestamp(t1.timestamp)) as months,
                    extract(day from to_timestamp(t1.timestamp)) as days, extract(hour from to_timestamp(t1.timestamp)) as hours,
                    trunc(extract(minute from to_timestamp(t1.timestamp))/5) as minutes_group,
                    case when t1.talk >= 4 and t1.talk <= 21 then 1 else 0 end as talk, t1.steps
                FROM public.gateway_silmeew20data t1
                WHERE to_timestamp(timestamp) >= %s and to_timestamp(timestamp) < %s and user_id = 2
            ) t2
          GROUP BY t2.years,t2.months,t2.days,t2.hours,t2.minutes_group
        ) t4
         ON t3.cur_year=t4.years and t3.cur_month=t4.months and t3.cur_day=t4.days and t3.cur_hour=t4.hours and t3.minutes_group = t4.minutes_group 
         ORDER BY t3.cur_year, t3.cur_month, t3.cur_day, t3.cur_hour, t3.minutes_group
         """

    week_sql = """
        SELECT case when t4.talk_sum is null then 0 else t4.talk_sum end as talk_sum,
            case when t4.steps_sum is null then 0 else t4.steps_sum end as steps_sum 
        FROM 
            (VALUES(extract(year from to_date(%s, 'YYYY-MM-DD HH24-MI-SS')), 
                extract(month from to_date(%s, 'YYYY-MM-DD HH24-MI-SS HH24-MI-SS')), 
                extract(day from to_date(%s, 'YYYY-MM-DD HH24-MI-SS'))),
            (extract(year from to_date(%s, 'YYYY-MM-DD HH24-MI-SS')+1), 
                extract(month from to_date(%s, 'YYYY-MM-DD HH24-MI-SS')+1), 
                extract(day from to_date(%s, 'YYYY-MM-DD HH24-MI-SS'))+1),
            (extract(year from to_date(%s, 'YYYY-MM-DD HH24-MI-SS')+2),
                extract(month from to_date(%s, 'YYYY-MM-DD HH24-MI-SS')+2),
                extract(day from to_date(%s, 'YYYY-MM-DD HH24-MI-SS'))+2),
            (extract(year from to_date(%s, 'YYYY-MM-DD HH24-MI-SS')+3),
                extract(month from to_date(%s, 'YYYY-MM-DD HH24-MI-SS')+3), 
                extract(day from to_date(%s, 'YYYY-MM-DD HH24-MI-SS'))+3),
            (extract(year from to_date(%s, 'YYYY-MM-DD HH24-MI-SS')+4),
                extract(month from to_date(%s, 'YYYY-MM-DD HH24-MI-SS')+4),
                extract(day from to_date(%s, 'YYYY-MM-DD HH24-MI-SS'))+4),
            (extract(year from to_date(%s, 'YYYY-MM-DD HH24-MI-SS')+5), 
                extract(month from to_date(%s, 'YYYY-MM-DD HH24-MI-SS')+5), 
                extract(day from to_date(%s, 'YYYY-MM-DD HH24-MI-SS'))+5),
            (extract(year from to_date(%s, 'YYYY-MM-DD HH24-MI-SS')+6), 
                extract(month from to_date(%s, 'YYYY-MM-DD HH24-MI-SS')+6), 
                extract(day from to_date(%s, 'YYYY-MM-DD HH24-MI-SS'))+6)) as t3 (cur_year, cur_month, cur_day) 
        LEFT JOIN 
        (
            SELECT t2.years,t2.months,t2.days,sum(t2.talk) as talk_sum, sum(t2.steps) as steps_sum 
            FROM 
                (SELECT 
                    extract(year from to_timestamp(t1.timestamp)) as years, extract(month from to_timestamp(t1.timestamp)) as months,
                    extract(day from to_timestamp(t1.timestamp)) as days,
                    case when t1.talk >= 4 and t1.talk <= 21 then 1 else 0 end as talk,t1.steps 
                FROM public.gateway_silmeew20data t1 
                WHERE to_timestamp(timestamp) >= %s and to_timestamp(timestamp) < %s
            ) t2 
            GROUP BY t2.years,t2.months,t2.days
        ) t4 
        on t3.cur_year=t4.years and t3.cur_month=t4.months and t3.cur_day=t4.days 
        order by t3.cur_year, t3.cur_month, t3.cur_day
        """

    last_sql = """
        SELECT uv, hr, skin_temp/256.0 as skin_temp, talk 
        FROM public.gateway_silmeew20data 
        WHERE timestamp 
        IN(
            SELECT max(timestamp) 
            FROM public.gateway_silmeew20data 
            WHERE to_char(to_timestamp(timestamp), 'YYYY-MM-DD') = %s
        )
      """
    
    pulse_day_sql = """
        SELECT min(motion_freq_avg)
        FROM
        (
            SELECT round(min(motion_freq_avg),2) as motion_freq_avg
            FROM
            (
                SELECT t4.motion_freq_avg
                FROM
                (
                    SELECT sum(t3.sum_flag) as sleep_state_sum, t3.group_flag, avg(t3.motion_freq) as motion_freq_avg
                    FROM
                        (SELECT t2.sleep_state as sum_flag, t1.timestamp as group_flag, t2.timestamp, t2.motion_freq
                        FROM
                            (SELECT * FROM public.gateway_silmeew20data 
                             WHERE to_timestamp(timestamp - 60) >= %s and to_timestamp(timestamp) < %s and user_id = 2
                            ORDER BY timestamp ASC ) t1,
                            (SELECT * FROM public.gateway_silmeew20data
                             WHERE to_timestamp(timestamp) >= %s and to_timestamp(timestamp) < %s and user_id = 2
                            ORDER BY timestamp ASC) t2
                        WHERE t1.sleep_state = 1 and (t2.timestamp >=t1.timestamp and t2.timestamp < t1.timestamp + 300)
                        ) t3
                    WHERE t3.group_flag != t3.timestamp
                    GROUP BY t3.group_flag
                ) t4
                WHERE t4.sleep_state_sum = 0
                order by t4.group_flag
            )t5
            union
            SELECT round(coalesce(min(motion_freq_avg),9999),2) as motion_freq_avg
            FROM
            (
                SELECT t4.motion_freq_avg
                FROM
                (
                    SELECT sum(t3.sum_flag) as sleep_state_sum, 
                           t3.group_flag, avg(t3.motion_freq) as motion_freq_avg
                    FROM
                        (SELECT t2.act_type as sum_flag, t1.timestamp as group_flag, t2.timestamp, t2.motion_freq
                        FROM
                            (SELECT * FROM public.gateway_silmeew20data 
                             WHERE to_timestamp(timestamp - 60) >= %s and to_timestamp(timestamp) < %s and user_id = 2
                            ORDER BY timestamp ASC ) t1,
                            (SELECT * FROM public.gateway_silmeew20data
                             WHERE to_timestamp(timestamp) >= %s and to_timestamp(timestamp) < %s and user_id = 2
                            ORDER BY timestamp ASC) t2
                        WHERE t1.sleep_state = 0 and t1.act_type != 0 and (t2.timestamp >=t1.timestamp and t2.timestamp < t1.timestamp + 300)
                        ) t3
                    WHERE t3.group_flag != t3.timestamp
                    GROUP BY t3.group_flag
                ) t4
                WHERE t4.sleep_state_sum = 0
                order by t4.group_flag
            ) t6
        ) t7
    """

    sleep_sql = """
        SELECT min(t4.start) as start, t4.end, min(t4.status) as status
        FROM
        (
            SELECT t3.group_flag, min(t3.start) as start, max(t3.end) as end, max(t3.status) as status
            FROM
            (
                SELECT t1.timestamp as start, t2.timestamp as end, t1.status as status, 
                       t2.status as status_tmp, t1.rid as group_flag, t2.rid, t2.input_time, t1.input_time, 
                       (t2.rid-t1.rid),
                       extract(epoch from t2.input_time) - extract(epoch from t1.input_time)
                FROM
                    (SELECT timestamp, body_motion,
                            date_trunc('minute', to_timestamp(timestamp)) as input_time,
                            case when body_motion = 0 then 2 else 1 end as status,
                            row_number() over(ORDER BY timestamp) rid
                    FROM public.gateway_silmeew20data
                    WHERE sleep_state = 1 and body_motion = 0 and to_timestamp(timestamp) >= %s and to_timestamp(timestamp) < %s and user_id = %s
                    ) t1,
                    (SELECT timestamp, body_motion,
                            to_timestamp(to_char(to_timestamp(timestamp), 'yyyy-mm-dd hh24:mi'), 'yyyy-mm-dd hh24:mi') as input_time,
                            case when body_motion = 0 then 2 else 1 end as status,
                            row_number() over(ORDER BY timestamp) rid
                    FROM public.gateway_silmeew20data
                    WHERE sleep_state = 1 and body_motion = 0 and to_timestamp(timestamp) >= %s and to_timestamp(timestamp) < %s and user_id = %s
                    ) t2
                WHERE (t2.rid-t1.rid)*60=extract(epoch from t2.input_time) - extract(epoch from t1.input_time) 
                      and t2.rid >= t1.rid and t1.status = t2.status
                ORDER BY t1.timestamp
            ) t3
            GROUP BY t3.group_flag
        ) t4
        GROUP BY t4.end
        union all
        SELECT min(t4.start) as start, t4.end, min(t4.status) as status
        FROM
        (
            SELECT t3.group_flag, min(t3.start) as start, max(t3.end) as end, max(t3.status) as status
            FROM
            (
                SELECT t1.timestamp as start, t2.timestamp as end, t1.status as status, 
                       t2.status as status_tmp, t1.rid as group_flag, t2.rid, t2.input_time, t1.input_time, 
                       (t2.rid-t1.rid),
                       extract(epoch from t2.input_time) - extract(epoch from t1.input_time)
                FROM
                    (SELECT timestamp, body_motion,
                            date_trunc('minute', to_timestamp(timestamp)) as input_time,
                            case when body_motion = 0 then 2 else 1 end as status,
                            row_number() over(ORDER BY timestamp) rid
                    FROM public.gateway_silmeew20data
                    WHERE sleep_state = 1 and body_motion != 0 and to_timestamp(timestamp) >= %s and to_timestamp(timestamp) < %s and user_id = %s
                    ) t1,
                    (SELECT timestamp, body_motion,
                            to_timestamp(to_char(to_timestamp(timestamp), 'yyyy-mm-dd hh24:mi'), 'yyyy-mm-dd hh24:mi') as input_time,
                            case when body_motion = 0 then 2 else 1 end as status,
                            row_number() over(ORDER BY timestamp) rid
                    FROM public.gateway_silmeew20data
                    WHERE sleep_state = 1 and body_motion != 0 and to_timestamp(timestamp) >= %s and to_timestamp(timestamp) < %s and user_id = %s
                    ) t2
                WHERE (t2.rid-t1.rid)*60=extract(epoch from t2.input_time) - extract(epoch from t1.input_time) 
                      and t2.rid >= t1.rid and t1.status = t2.status
                ORDER BY t1.timestamp
            ) t3
            GROUP BY t3.group_flag
        ) t4
        GROUP BY t4.end
    """

    def get_sql(self, type=CommonStr.DAY):
        sql = self.pulse_day_sql

        if type == CommonStr.DAY:
            sql = self.day_sql
        elif type == CommonStr.WEEK:
            sql = self.week_sql
        elif type == CommonStr.DAY_LAST_VALUE:
            sql = self.last_sql
        return sql
