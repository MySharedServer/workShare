# Submit Code
> **git status**
>
> **git add .** or **git add _\<file1, file2, ...\>_**
> 
> **git commit -m 'xxx'**
>
> **git push origin _\<branchName\>_**

# Cancle stage modifed content
> replace with remote branch 
>
> **git reset HEAD**
>
> delete modifed content
>
> **git rm --cached _\<file1, file2, ...\>_**
>
> **git reset --mixed --soft --hard  > soft (commit) < mixed (commit + add) < hard (commit + add + local working)

# Override stage and local workspace with remote branch
> **git checkout HEAD .**
>
> **git checkout HEAD _\<file1, file2, ...\>_**

# Sync remote branch
> **git fetch origin _\<branchName\>_**  >> no merge remote
>
> **git pull origin _\<branchName\>_** >> get remote branch and merge to local branch

# Compare different
> **git diff**  > show diff between staged changes and local work
>
> **git diff --cached**  >> show diff of staged changes
>
> **git diff --left-right [branchA]...[branchB]**

# Merge branch
> **git merge _\<branchName\>_**  >> merge \<branchName\> to current branch

# Watch Log
> **git log --graph**
>
> **git log --grep=keywords**  >> filter from commit log
>
> **git log --author=[username]** >> filter with username
