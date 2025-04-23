---
title: Docker-容器化
date: 2024-10-12 01:57:22
lastmod: 2024-10-12 01:57:22
aliases: 
keywords: 
categories:
  - 开发工具
tags:
  - 容器化
share: true
---



# 容器化

**容器化**：将一个程序所需的运行库、依赖等打包到一起，以便可以到处运行
- 容器化 vs 虚拟机：容器化不含操作系统，且资源占用小
- 容器化案例：一个网站，前端 Vue 后端 Spring+MySQL，Docker 可以将 NodeJS、Java、Spring、MySQL 等通通打包到一个镜像中直接运行

用途：
- 解决开发环境的配置问题
- 实现一键部署


## Docker 体系结构
- 镜像：相当于类，只读
- 容器：镜像的实例
- docker-daemon：处理客户端的请求，并返回结果
![L|800](./assets/Docker-%E5%AE%B9%E5%99%A8%E5%8C%96/image-2023-08-23_09-52-08-386.png)

### 镜像

镜像中包含以下内容：
- 精简版操作系统
- 运行时环境：如 NodeJS、Java
- 应用程序、应用程序的第三方依赖库
- 环境变量

**镜像数据持久化**：
- 默认不会储存数据，容器关闭时会删除容器运行时创建的所有文件
- 指定容器卷 DockerVolume，将容器目录映射到宿主目录，从而实现持久化


### Docker Compose

概述：一个程序可能需要用到一组相互关联的应用程序，如前后端、数据库。这些程序分别部署在不同的 Docker 镜像中，而 DockerCompose 用于解决关联启动的问题，实现一键启动所有服务
- Docker Compose 用于定义和运行多容器应用程序
- 使用 docker-compose.yml 配置

# 使用 Docker


## 安装与配置
### 配置镜像

1. Linux 环境下安装的 docker：
```shell
$ sudo vi /etc/docker/daemon.json
```
添加 registry-mirrors，这里只使用了 Docker 中国区的镜像，若没有上述文件新建一个即可：
```JSON
{
 "registry-mirrors": ["https://registry.docker-cn.com"]
}
```

Docker Desktop：找到 Docker Destop -> Preferences -> Docker Engine，添加镜像配置即可
![L|800](./assets/Docker-%E5%AE%B9%E5%99%A8%E5%8C%96/image-2023-08-23_13-05-25-970.png)



## 基础使用

**创建 Docker 容器**：
- 创建 Dockefile，其中包含构建容器所需的各种指令
- 使用 Dockerfile 构建镜像
- 使用镜像创建容器

### 创建 Dockerfile

```Dockerfile
# 前端开发中，时常需要使用 shell 命令，而有一个较为完整的环境比较重要，因此选择了使用 ubuntu 作为基础，若在意容器大小的话，可自行选择适用的基础镜像
FROM ubuntu
LABEL org.opencontainers.image.authors="codebaokur@codebaoku.com"
# 设置环境变量 
ENV DEBIAN_FRONTEND noninteractive
# 设置时区
ARG TZ=Asia/Shanghai
ENV TZ ${TZ}
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# 用 root 用户操作
USER root

# 更换阿里云源，在国内可以加快速度
RUN sed -i "s/security.ubuntu.com/mirrors.aliyun.com/" /etc/apt/sources.list && \
    sed -i "s/archive.ubuntu.com/mirrors.aliyun.com/" /etc/apt/sources.list && \
    sed -i "s/security-cdn.ubuntu.com/mirrors.aliyun.com/" /etc/apt/sources.list &&\
    apt-get clean

# 更新源，安装相应工具
RUN apt-get update && apt-get install -y \
    zsh \
    vim \
    wget \
    curl \
    python \
    git-core

#  安装 zsh，以后进入容器中时，更加方便地使用 shell
RUN git clone https://github.com/robbyrussell/oh-my-zsh.git ~/.oh-my-zsh && \
    cp ~/.oh-my-zsh/templates/zshrc.zsh-template ~/.zshrc && \
    git clone https://github.com/zsh-users/zsh-autosuggestions ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-autosuggestions && \
    git clone https://github.com/zsh-users/zsh-syntax-highlighting.git ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-syntax-highlighting && \
    sed -i 's/^plugins=(/plugins=(zsh-autosuggestions zsh-syntax-highlighting z /' ~/.zshrc && \
    chsh -s /bin/zsh

# 创建 me 用户
# RUN useradd --create-home --no-log-init --shell /bin/zsh -G sudo me && \
#     adduser me sudo && \
#     echo 'me:password' | chpasswd

# 为 me 安装 omz
# USER me
# RUN git clone https://github.com/robbyrussell/oh-my-zsh.git ~/.oh-my-zsh && \
#     cp ~/.oh-my-zsh/templates/zshrc.zsh-template ~/.zshrc && \
#     git clone https://github.com/zsh-users/zsh-autosuggestions ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-autosuggestions && \
#     git clone https://github.com/zsh-users/zsh-syntax-highlighting.git ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-syntax-highlighting && \
#     sed -i 's/^plugins=(/plugins=(zsh-autosuggestions zsh-syntax-highlighting z /' ~/.zshrc

# 安装 nvm 和 node
ENV NVM_DIR=/home/me/.nvm \
    NODE_VERSION=v14
RUN mkdir -p $NVM_DIR && \
    curl -o- https://gitee.com/mirrors/nvm/raw/master/install.sh | bash && \
    . $NVM_DIR/nvm.sh && \
    nvm install ${NODE_VERSION} && \
    nvm use ${NODE_VERSION} && \
    nvm alias ${NODE_VERSION} && \
    ln -s `npm bin --global` /home/me/.node-bin && \
    npm install --global nrm && \
    nrm use taobao && \
    echo '' >> ~/.zshrc && \
    echo 'export NVM_DIR="$HOME/.nvm"' >> ~/.zshrc && \
    echo '[ -s "$NVM_DIR/nvm.sh" ] && . "$NVM_DIR/nvm.sh"  # This loads nvm' >> ~/.zshrc

# 安装 yarn
RUN curl -o- -L https://yarnpkg.com/install.sh | bash; \
    echo '' >> ~/.zshrc && \
    echo 'export PATH="$HOME/.yarn/bin:$PATH"' >> ~/.zshrc

# Add NVM binaries to root's .bashrc
USER root
RUN echo '' >> ~/.zshrc && \
    echo 'export NVM_DIR="/home/me/.nvm"' >> ~/.zshrc && \
    echo '[ -s "$NVM_DIR/nvm.sh" ] && . "$NVM_DIR/nvm.sh"  # This loads nvm' >> ~/.zshrc && \
    echo '' >> ~/.zshrc && \
    echo 'export YARN_DIR="/home/me/.yarn"' >> ~/.zshrc && \
    echo 'export PATH="$YARN_DIR/bin:$PATH"' >> ~/.zshrc

# Add PATH for node & YARN
ENV PATH $PATH:/home/me/.node-bin:/home/me/.yarn/bin

# 删除 apt/lists，可以减少最终镜像大小
RUN rm -rf /var/lib/apt/lists/*
WORKDIR /var/www
```

### 构建镜像

```shell
docker build -t frontend/react:v1 .
```
#### 运行容器

使用 `docker run -d 镜像 --name CONTAINER_NAME` 命令后台运行容器
使用 `docker exec -it CONTAINER_NAME /bin/bash` 命令以交互式终端访问容器

格式如下：
```shell
$ docker run 镜像:标签 命令
$ docker exec -it 容器名 程序
# 以 me 身份运行，推荐方式
docker run --user=me -it frontend/react:v1 /bin/zsh

# 以 root 角色运行
docker run -it frontend/react:v1 /bin/zsh
```

### 编写 docker-compose.yml

在开发时，我们寻常需要多个容器配合使用，比如需要配合 mysql 或其他容器使用时，使用 docker-compose.yml 可以更好的组织他们。
```YAML
version: '2'
services:
    react:
	    build:
	        context: .
	        dockerfile: react/Dockerfile
	    tty: true
	    ports:
	        - 30000:3000
	    volumes:
	        - ./react/www:/var/www
	    networks:
	        - frontend
    mysql:
	    image: mysql:5.7
	    ports:
	        - 33060:3306
	    volumes:
	        - ./mysql/data:/var/lib/mysql
	        - ./mysql/docker-entrypoint-initdb.d:/docker-entrypoint-initdb.d
	    environment:
	        - MYSQL_ROOT_PASSWORD=password
	    networks:
	        - frontend

# 将容器置于同一 networks 即可直接通过容器名访问
networks:
    frontend:
    driver: bridge    
```

### 启动容器

```sh
# 进入 docker-compose.yml 所在目录
$ cd frontend

# 后台启动 docker-compose.yml 中所有容器，若容器没有构建则会先构建
$ docker-compose up -d

# 进入 react 容器中，以便命令行交互
$ docker-compose exec --user=me react /bin/zsh
```

## More

Docker-命令

Dockerfile

Docker-Compose

Docker-network-网络