# Git cheatsheet

## Index
- [Basic workflow](#basic-workflow)
- [Branches](#branches)
- [Tags](#tags)
- [Stash](#stash)
- [Upload an existing repo](#upload-an-existing-repo)
- [Revert to a previous commit](#revert-to-a-previous-commit)
- [Download only specific folders from a repo](#download-only-specific-folders-from-a-repo)

## Basic workflow

The usual workflow consists in updating your local repository from your remote repo, such as GitHub; then you work on your project; and finally, you commit and push your local changes to the remote repository.  

First check for a possible update in the remote repository:  
`git fetch`  

If so, download updates from the remote repo:  
`git pull`  

...Then work on your code, etc...  

Check the local changes  
`git status`  

Add the local changes  
`git add .`  

Commit your local changes  
`git commit -m "comment"`  

Optional:  
`git commit --amend` (change the most recent commit message)  
`git tag <tag_name> HEAD` (include a release tag)  

Push your local commits to the remote repo  
`git push` or  
`git push --tags` or  
`git push origin main --tags` (if on main branch)  

## Branches

Show current branch:  
`git branch --show-current`  

See all local branches:  
`git branch`  
See all branches, local and remote:  
`git branch -a`  

Create a new branch:  
`git branch <BRANCH>`  
Or if you’d like to start at a specific revision, add that revision’s hash at the end of the command,  
`git branch <BRANCH> 2b504bee`  

Switch to a new branch:  
`git switch <BRANCH>` or  
`git checkout <BRANCH>`  
Switch to a remote branch:  
`git checkout --track origin/<BRANCH>`  

Publish the local branch:  
`git push -u origin <BRANCH>`  

Merge the branch to the main:  
`git switch main`  
`git merge <BRANCH>`  

Delete remote branch ('`<remote_name>`' is usually '`origin`'):  
`git push -d <remote_name> <branchname>`  
Delete local branch:  
`git branch -d <branchname>`  

## Tags

It is recommended to use tags following [semantic versioning](https://semver.org/), as in:  
`v<major>.<minor>.<patch>`  

To check the tags of the project,  
`git tag -n`  

To create a new tag for the latest commit,  
`git tag <tag_name> HEAD`  

Or to create the tag with a message,  
`git tag -a <tag_name> HEAD -m "message"`  

Git push does not push the tags. If I am in a branch other than Main, it has to be done as:  
`git push --tags`  
Or if I am on main branch, push as  
`git push origin main --tags`  

To create a git tag for a specific previous commit, first check the commit SHA (the weird numbers):  
`git log --oneline`  
`git tag <tag_name> <commit_sha>`  
Or with a message,  
`git tag -a <tag_name> <commit_sha> -m "message"`  

To delete local tags,  
`git tag --delete <tag_name>`  
And to delete remote tags,  
`git push --delete origin <tag_name>`  

## Stash

To pull and update your local repo from the remote one, with uncommited local changes:  
`git stash`  
`git pull`  

Depending if you want to apply or discard the stashed changes:  
`git stash apply` OR `git stash clear`  

## Upload an existing repo

Make a git repository in your existing work:  
`git init`  
`git add .`  
`git commit -m "initial commit"`  

Add the new remote origin:  
`git remote add origin git@github.com:pablogila/NEW_PROJECT.git`  

Push to GitHub so that next time you can push as always:  
`git push -u -f origin main`  

## Revert to a previous commit

You can revert to the last commit with a stash, if there were no new commits.  

To revert to a previous commit, see the lasts ones, and revert to the desired commit:  
`git log`  
`git revert <commit_hash>`  

## Download only specific folders from a repo

Sometimes an online repository might be several GBs in size, but you may only need a single folder. Don't worry, you don't need to download the whole repo!  

An easy way to download a single folder is to paste its permalink into [DownGit](https://downgit.evecalm.com/).  

If you still prefer to use the terminal,  
```bash
mkdir <repo>
cd <repo>
git init
git remote add -f origin <url>
git config core.sparseCheckout true
echo "some/dir/" >> .git/info/sparse-checkout
echo "another/sub/tree" >> .git/info/sparse-checkout
git pull origin master
```

