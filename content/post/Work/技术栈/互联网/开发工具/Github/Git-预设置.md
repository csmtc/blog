---
title: Git-预设置
date: 2023-02-07 16:05:55
lastmod: 2025-02-07 16:05:55
aliases: 
keywords: 
categories:
  - 开发工具
tags: 
share: true
---


#### Who are you?
Every Git commit includes the author’s name and e-mail. Make sure Git knows your name and email by running these two commands:
```
git config --global user.name "csmtc"
git config --global user.email csmtc@outlook.com
```

#### git log
git log is a command for looking at the history of your repository.
To create a special version of git log that summarizes the history of your repo, let’s create a git lol alias using the command (all on one line):
```
git config --global alias.lol "log --graph --oneline --decorate --color --all"
```
Now, in any repository you can use:
```
git lol
```
to see an ASCII-art graph of the commit history.

#### 代理
代理协议支持 http，https，socks5 等
```
git config --global http.proxy http://127.0.0.1:57890
```

#### check
To confirm that you set up Git properly, run
```
git config --list
```
and look for the settings you made in its output:


#### 测试连接
```
ssh -T git@github.com
ssh -T git@gitee.com
```