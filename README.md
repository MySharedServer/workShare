# Submit Code
> **git status**
>
> **git add .** or **git add _\<file1, file2, ...\>_**
> 
> **git commit -m 'xxx'**
>
> **git push origin _\<branchName\>_**

# Cancle stage modifed content
> *replace with remote branch
> **git reset HEAD**
>
> *delete modifed content
> **git rm --cached _\<file1, file2, ...\>_**
>
> **git reset --mixed --soft --hard**  *soft (commit) < mixed (commit + add) < hard (commit + add + local working)*

# Override stage and local workspace with remote branch
> **git checkout HEAD .**
>
> **git checkout HEAD _\<file1, file2, ...\>_**

# Sync remote branch
> *no merge remote
> **git fetch origin _\<branchName\>_**
>
> *get remote branch and merge to local branch
> **git pull origin _\<branchName\>_**

# Compare different
> *show diff between staged changes and local work
> **git diff**
>
> *show diff of staged changes
> **git diff --cached**
>
> *show two branch diff
> **git diff --left-right [branchA]...[branchB]**

# Merge branch
> *merge \<branchName\> to current branch
> **git merge _\<branchName\>_**

# Watch Log
> **git log --graph**
>
> *filter from commit log
> **git log --grep=keywords**
>
> *filter with username
> **git log --author=[username]**
