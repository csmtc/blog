---
title: Git分支操作
date: 2023-03-28 14:46:35
lastmod: 2025-03-12 21:52:42
aliases: 
keywords: 
categories:
  - 开发工具
tags:
  - Git
share: true
---



在 Git 中，分支操作是一个非常重要的部分，它允许你在开发过程中创建、合并和删除分支，以便更好地管理代码的不同版本和功能。以下是一些常见的 Git 分支操作及其用法：

### 1. 创建分支

创建一个新的分支：

```bash
git branch <branch_name>
```

例如：

```bash
git branch feature-xyz
```

### 2. 切换分支

切换到指定分支：

```bash
git checkout <branch_name>
```

例如：

```bash
git checkout feature-xyz
```

从Git 2.23版本开始，你可以使用更直观的 `git switch` 命令：

```bash
git switch <branch_name>
```

### 3. 创建并切换到新分支

创建并切换到新分支：

```bash
git checkout -b <branch_name>
```

或者：

```bash
git switch -c <branch_name>
```

### 4. 查看分支

列出所有分支：

```bash
git branch
```

列出所有远程分支：

```bash
git branch -r
```

列出所有本地和远程分支：

```bash
git branch -a
```

### 5. 合并分支

将指定分支合并到当前分支：

```bash
git merge <branch_name>
```

例如：

```bash
git merge feature-xyz
```

### 6. 删除分支

删除本地分支：

```bash
git branch -d <branch_name>
```

强制删除本地分支（即使未被合并）：

```bash
git branch -D <branch_name>
```

删除远程分支：

```bash
git push origin --delete <branch_name>
```

### 7. 重命名分支

重命名当前分支：

```bash
git branch -m <new_branch_name>
```

重命名指定分支：

```bash
git branch -m <old_branch_name> <new_branch_name>
```

### 8. 分支的跟踪和推送

推送本地分支到远程仓库：

```bash
git push origin <branch_name>
```

设置本地分支与远程分支的跟踪关系：

```bash
git branch --set-upstream-to=origin/<branch_name>
```

### 9. 分支比较

比较两个分支之间的差异：

```bash
git diff <branch_name_1> <branch_name_2>
```

### 10. 分支图

查看分支历史图：

```bash
git log --oneline --graph --all
```

### 11. 获取远程分支

获取远程仓库的所有分支信息：

```bash
git fetch
```

### 12. 检查分支合并状态

查看分支是否已被合并：

```bash
git branch --merged
git branch --no-merged
```

这些操作可以帮助你在 Git 中有效地管理分支，使团队协作更加顺畅，并确保代码版本的清晰和可追溯性。