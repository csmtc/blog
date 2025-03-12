---
title: Git-工作流
date: 2023-02-07 14:46:35
lastmod: 2024-09-28 14:46:35
aliases: 
keywords: 
categories:
  - 设计模式
tags: 
share: true
---



说明：本文所有`master`均可以用`main`替代

## 概念

**VCS**：Version control is a system that records changes to a file or set of files over time
**用途**：Git is a version control system (VCS). The Pro Git book describes what Git is used for：
- you can recall specific versions later (recall selected files or entire project)
- compare changes over time
- see who last modified something that might be causing a problem
- if you screw things up or lose files, you can easily recover.

Some of the most important Git concepts:
- **repository**: A folder containing all the files associated with a project (e.g., a 6.031 problem set or team project), as well as the entire history of commits to those files.
- **commit** (or “revision”): A snapshot of the files in a repository at a given point in time. The **basic building block of data** in Git
- **add** (or “stage”): Before changes to a file can be committed to a repository, the files in question must be added or staged (before each commit). This lets you commit changes to only certain files of your choosing at a time, but can also be a bit of a pain if you accidentally forget to add all the files you wanted to commit before committing.
- **clone**: Since Git is a “distributed” version control system, there is no concept of a centralized Git “server” that holds the latest official version of your code. Instead, developers “clone” remote repositories that contain files they want access to, and then commit to their local clones. Only when they push their local commits to the original remote repository are other developers able to see their changes.
- **push**: The act of sending your local commits to a remote repository. Again, until you add, commit, and push your changes, no one else can see them.
- **pull**: The act of retrieving commits made to a remote repository and writing them into your local repository. This is how you are able to see commits made by others after the time at which you made an initial clone.

## 基本操作

#### Cloning
open the terminal (use Git Bash on Windows) and use the cd command to change to the directory where you would like to store your code. Then run:

```
git clone URI-of-remote-repo
```
or
```
git clone URI-of-remote-repo project-name
```
The result will be a new directory project-name with the contents of the repository. This is your local repository.

#### Creating a commit

The **basic building block of data** in Git is called a “commit”. A commit represents some change to one or more files (or the creation or deletion of one or more files).

When you change a file or create a new file, that change is not part of the repository. Adding it takes two steps. 
First, run:
```
git add file. txt (where file. txt is the file you want to add,maybe need include file path)
```

This stages the file. Second, once you’ve staged all your changes, run:
```
git commit
```
This will pop up the editor for your commit message. When you save and close the editor, the commit will be created.

#### status
Git has some nice commands for seeing the status of your repository.

The most important of these is `git status` . Run it any time to see *which files Git sees have been modified and are still unstaged* and which files have been modified and staged (so that if you git commit those changes will be included in the commit). 
> Note that the same file might have both staged and unstaged changes, if you *modified the file again after running git add*.

When you have unstaged changes, you can see what the changes were (relative to the last commit) by running `git diff` . Note that this will not include changes that were staged (but not committed). You can see those by running git diff --staged.

#### Pushing

After you’ve made some commits, you’ll want to push them to a remote repository. Simplely, you should have only one remote repository to push to, called origin. To push to it, you run the command:
```
git push origin main
```

The origin in the command specifies that you’re pushing to the origin remote. By convention *传统的*, that’s the remote repository you cloned from.

The main refers to the main branch, the default branch in our Git repositories. We won’t use branches other than main in 6.031. All our commits will be on main, and that’s the branch we want to push.

### Merges
Sometimes, when you try to push, things will go wrong. You might get an output like this:
```
! [rejected]      main -> main (non-fast-forward)
```
What’s going on here is that Git won’t let you push to a repository unless *all your commits come after all the ones already in the remote repository*. If you get an error message like that, it means that there is a commit in your remote repository that you don’t have in your local one (on a project, probably because a teammate pushed before you did). If you find yourself in this situation, you *have to pull first and then push*.

#### Pulling

run `git pull`. When you run this, Git actually does two things:
1. It downloads the changes and stores them in its internal state. 
   At this point, the repository doesn’t look any different, but it knows what the state of the remote repository is and what the state of your local repository is.
2. It incorporates *合并* the changes *from the remote repository into the local* repository by *merging*, described below.

#### Merging

If you made some changes to your repository and you’re trying to incorporate the changes from another repository, you need to merge them together somehow. In terms of commits, what actually needs to happen is that you have to *create a special merge commit that combines both changes*. How this process actually happens depends on the changes:

- **don’t conflict**: If you’re lucky, then the changes you made and the changes that you downloaded from the remote repository don’t conflict. For example, maybe *you changed one file and your project partner changed another*. In this case, it’s safe to just include both changes. Similarly, maybe you *changed different parts of the same file*. **In these cases, Git can do the merge automatically**. When you run git pull, it will pop up an editor as if you were making a commit: this is the commit message of the merge commit that Git automatically generated. Once you save and close this editor, the merge commit will be made and you will have incorporated both changes. At this point, you can try to git push again.

- **Merge conflicts**: Sometimes, you’re not so lucky. If the changes you made and the changes you pulled *both edit the same part of the same file*, Git won’t know how to resolve it. This is called a merge conflict. In this case, you will get an output that says CONFLICT in big letters. If you run `git status`, it will show the conflicting files with the label `Both modified`. You now have to edit these files and resolve them by hand.

	- First, open the files in Visual Studio Code. The parts that are conflicted will be really obviously marked with obnoxious `<<<<<<<<<<<<<<<<<<` , `==================,` and `>>>>>>>>>>>>>>>>>>` lines. Everything between the `<<<<` and the `====` lines are the changes *you made*. Everything between the `====` and the `>>>>` lines are the changes *you pulled in*. It’s your job to figure out how to combine these. The answer will of course depend on the situation. Maybe one change logically supercedes the other, or maybe they can be merged somehow. You should *edit* the file to your satisfaction and *remove* the `<<<</====/>>>>` markers when you’re done.
	- Once you have resolved all the conflicts (note that there can be several conflicting files, and also several conflicts per file), `git add` all the affected files and then `git commit`. You will have an opportunity to write the merge commit message (where you should describe how you did the merge). Now you should be able to `push`.

- **Avoid merges** and merge conflicts: Pull before you start working
  Before you start working, always git pull. That way, you’ll be working from the latest version of your code, and you’ll be less likely to have to perform a merge later.

### Getting the history of the repository

You can see the list of all the commits in the repository (with their commit messages) using `git log`. You can see the last commit on the repository using git show. This will show you the commit message as well as all the modifications.

**Long output**: if git log or git show generate more output than fits on one page, you will see a colon (:) symbol at the bottom of the screen. You will not be able to type another command! Use the arrow keys to scroll up and down, and quit the output viewer by pressing q. (You can also press h for see the viewer’s other commands, but scrolling and quitting are the most important to know.)

**Commit IDs**: every Git commit has a unique ID, the hexadecimal numbers you see in git log or git show. The commit ID is a unique cryptographic *密码的,=crypto* hash of the contents of that commit. Every commit, not just within your repository but within the universe of all Git repositories, has a unique ID (with extremely high probability).

You can reference a commit by its ID (usually just by the first few characters). This is useful with a command like `git show`, where you can look at a particular commit rather than only the most recent one.

### git revert

revert a commit or commit between commitA and commitB
```
git revert -n commit-id
git revert -n commit-idA..commit-idB
```
不使用-n，指令后会弹出编辑器用于编辑提交信息，使用-n 参数， revert 后需要重新提交一个 commit。

回退时出现冲突：
- git revert --abort，合并冲突后退出，当前的操作会回到指令执行之前的样子
- git revert --quit，合并后退出，但是保留变化

## 流程
### 将仓库复制到本地

1. way2：下载
2. way1：clone 命令

### 修改代码


为保证不回滚master分支，因而创建feature分支再clone

1. 在本地创建并修改分支feature  
	创建名为`feature`的分支：`git checkout -b feature`  
	查看差异：`git diff`  
	提交文件到暂存区：`git add <changed_file_name>`  
	提交：`git commit`
2. 提交修改的feature分支到github：此过程中远端仓库可能已经更新，因而首先更新本地的master分支
	1. 切换到本地master分支：`git checkout master`
	2. PULL远端master：`git pull origin master`
	3. 将远端对master的修改合并到feature分支（相当于用最新的master分支创建了feature分支）：`git rebase master`
3. 将修改提交到github：`git push -f origin feature`（由于rebase了，所以需要-f强制）
4. 发送pull-request请求将feature分支合并到主分支
5. Squash and merge：为了保持主分支commit的简洁，尽量让每次commit后的都是可以正常工作的版本，通常用此命令将feature分支上的改变合并为一个改变
6. 至此远端更新完成，删除feature分支
	1. 删除远端分支
	2. 删除本地分支：先切换到本地主分支，再`git branch -D feature`
7. 拉取远程master分支：`git pull origin master`  
``
