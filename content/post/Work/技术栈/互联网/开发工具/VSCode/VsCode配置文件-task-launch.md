---
title: VsCode配置文件-task-launch
date: 2023-09-28 14:46:34
lastmod: 2025-03-12 21:53:36
aliases: 
keywords:
  - VSCode
  - 配置文件
categories:
  - 开发工具
tags:
  - VSCode
share: true
---


# Vscode 配置文件

vscode 使用的最基本的两个配置文件是**tasks.json**和**launch.json**文件（这两个文件一般都是在 vscode 当前打开的文件夹下的 .vscode 文件夹中，没有可以手动创建，只要位置正确就可以生效）。

**launch.json：** 这个配置文件是告诉vscode如何来启动调试你的代码程序的，这其中包括你的程序在哪个位置，你用什么工具来调试，调试的时候需要给调试工具传什么参数等。  
**tasks.json：** 这个配置文件是用来执行你预定的任务的，比如说你修改了你的代码，调试之前，肯定要重新生成新的程序后再调试，那么你就可以配置它告诉vscode怎么重新生成这个新的程序。(task.json不是必须文件，比如python调试，可以不用提前编译)

vscode就是先跑 tasks.json 任务，再跑 launch.json。

**说明：** vscode 调用任务是根据**lable**标签识别的(文章后面有说明)。

```cpp
"lable": "startRun"
```
## 环境变量

- ${workspaceFolder}：在 Visual Studio Code 中打开的文件夹的完整路径
- ${workspaceFolderBasename}：在Visual Studio Code中打开的文件夹名
- ${file}：当前打开的文件的完整路径
- ${relativeFile}：当前打开的文件的相对workspaceFolder路径
- ${relativeFileDirname}：当前打开的文件的文件夹的相对workspaceFolder路径
- ${fileBasenameNoExtension}：当前打开的文件的文件名，不包含扩展名
- ${fileDirname}：当前打开的文件的文件夹的完整路径
- ${fileExtname}：当前打开的文件的扩展名
- ${cwd}：Task启动时的工作目录
- ${lineNumber}：当前光标的所在的行号
- ${selectedText}：当前打开的文件中选中的文本
- ${execPath}：Visual Studio Code可知行文件的完整路径
- ${defaultBuildTask}：默认的Build Task的名字
- ${env:Name}：引用环境变量
- ${config:Name}：可以引用Visual Studio Code的设置项
- ${input:variableID}：传入输入变量

## Launch

以 C++编译为例：
- 指定 Linux，Windows 属性，设置每个平台运行的指令
- cwd 指定工作目录
- preLaunchTask 指定预载任务
```json
{
    // 使用 IntelliSense 了解相关属性。 
    // 悬停以查看现有属性的描述。
    // 欲了解更多信息，请访问: https://go.microsoft.com/fwlink/?linkid=830387
    "version": "0.2.0",
    "configurations": [
        {
            "name": "DefaultTest",
            "type": "lldb", 
            "request": "launch",
            "program": "${workspaceFolder}/build/${workspaceRootFolderName}_test",
            "osx": {
                "name": "TestOSX",
                "type": "lldb", 
                "request": "launch",
                "program": "${workspaceFolder}/build/${workspaceRootFolderName}_test",
            },
            "linux": {
                "name": "TestLinux",
                "type": "cppdbg",
                "request": "launch",
                "program": "${workspaceFolder}/build/${workspaceRootFolderName}_test",
                "MIMode": "gdb",
                "setupCommands": [
                    {
                        "description": "gdb print",
                        "text": "-enable-pretty-printing",
                        "ignoreFailures": true
                    }
                ],
            },
            "windows": {
                "name": "TestWindows",
                "type": "cppvsdbg",
                "request": "launch",
                "program": "${workspaceFolder}/build/Debug/${workspaceRootFolderName}_test"
            },
            "args": [], 
            "cwd": "${workspaceFolder}",
            "preLaunchTask": "CmakeBuild",
        },
    ]
}



```


## Task

### 1. Task 中一些主要的属性及相应语义：
- label：在用户界面上展示的 Task 标签
- type：Task的类型，分为shell和process两种
	- shell：作为Shell命令运行
	- process：作为一个进程运行
- command：真正执行的命令
- windows：Windows中的特定属性。相应的属性会在Windows中覆盖默认的属性定义。
- group：定义Task属于哪一组
- presentation：定义用户界面如何处理Task的输出
- options：定义cwd（当前工作目录）、env（环境变量）和shell的值
- runOptions：定义Task何时运行及如何运行。 

### 2. 控制 Task 在运行时的输出行为：
- reveal：控制集成终端是否显示
	- always：集成终端总是会在Task启动时显示
	- never：集成终端不会主动显示
	- silent：当输出不是错误和警告时，集成终端才会显示
- focus：控制集成终端在显示时是否取得焦点
- echo：控制被执行的命令是否在集成终端中输出
- showReuseMessage：控制是否显示显示“Terminal will be reused by tasks,press any key to close it”提示信息
- panel：控制不同的Task在运行时是否共享同一个集成终端
	- shared：共享集成终端
	- dedicated：Task会有一个专用的集成终端
	- new：每次运行的Task都会创建一个新的集成终端
- clear：控制Task在运行前，是否清除集成终端的输出
- group: 控制 Task 是否在同一个集成终端中运行

### 3. 控制 Task 在运行时的运行行为
- reevaluateOnRerun：在执行 Rerun Last Task 命令时，控制是否重新计算变量
- runOn：指定何时运行Task
	- default：只有在运行RunTask命令时，才会触发运行
	- foderOpen：当包含这个tasks.json文件夹被打开时，便会触发运行
### 示例
- 指定 dependson 属性，设置前置任务
```json
{
    "tasks": [
        {
            // 任务一： 创建 build 文件夹
            "type": "shell",
            "label": "CreateBuildDir", // lable 标记任务名称
            "command": "mkdir",  // 命令
            // 传给上面命令的参数，这里是传给 Unix 系统的参数，windows下稍有不用，下边有
            "args": [
                "-p",
                "build"
            ], 
            "windows": {
                "options": {
                    "shell": {
                        "executable": "powershell.exe"
                    }
                },
                "args": [   // 对于windows系统，传的参数
                    "-Force",
                    "build"
                ]
            },
            "options": {
                "cwd": "${workspaceFolder}"
            },
            "problemMatcher": [
                "$gcc"
            ],
        },
        // 任务二： Cmake
        // 在 build 文件夹中调用 cmake 进行项目配置
        // 如果想配置比如 release 还是 debug 可以添加参数或者在
        // CMakeLists.txt中设置也行
        {
            "type": "shell",
            "label": "cmakeRun", // 给这个任务起个名字
			// 这里的cmake，用我后面小程序创建的结果填的是全路径，
			// 命令写全路径，则路径中不能包含带空格
			// 如果你添加了环境变量，那么直接填写命令即可，也不会有
			// 路径是否包含空格的问题（下面的命令同理）
            "command": "cmake",
            "args": [
            	"-DCMAKE_MAKE_PROGRAM=E:\\Resource\\mingw64\\bin\\mingw32-make.exe", // MinGW目录下bin目录下的mingw32-make.exe
                "-G",
                // 不使用-G "Unix Makefiles" 参数可能会编译成了VS用的工程文件
                // 之所以三个斜杠，是因为vscode终端自己还要转义一次
                // 2021-01-21更新：我在32位的win7上发现，vscode自己又不转义了
                // 所以如果以下三个斜杠不行的话，大家手动改成一个斜杠就好，即\"Unix Makefiles\"
                // 后面我给的小程序默认写的是3个
                "\\\"Unix Makefiles\\\"",  
                "../"  // ../ 表示build文件夹的上级目录，CMakeLists.txt就放在上级目录中
            ],
            "options": {
                "cwd": "${workspaceFolder}/build"
            },
            "dependsOn":[
                "CreateBuildDir"  // 表示在 创建目录 任务结束后进行
            ]
        },
        // 任务三： make编译
        {
            "type": "shell",
            "label": "makeRun",
            "command": "mingw32-make",  // 这个也是MinGW目录下bin目录下的mingw32-make.exe，如果添加了环境变量，这里直接写mingw32-make.exe
            "args": [],
            "options": {
                "cwd": "${workspaceFolder}/build"
            }, // 注意这里是编译到了项目文件夹下的 build 文件夹里面，这里就解释了
            // 为什么 launch.json 中 program 路径要那么设置了。
            "dependsOn":[
                "cmakeRun"  // 表示在Cmake任务结束后进行
            ]
        },
    ],
    "version": "2.0.0"
}

```
