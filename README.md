# fastapi-vue-appscheduler

### 介绍
在线demo: http://60.204.224.115:8000/
支持app 管理 + app 调度, 这里app 指的是具有指定结构的python项目。
安装app时，会自动根据项目地址(目前仅支持svn)下载python项目，然后基于requirements.txt 安装依赖。

### 项目分支介绍
master主干维护公共代码，如用户管理、应用分类、项目管理 等
目前有2个项目分支，他们的主要区别如下：
web分支：app管理如安装、运行、调度都在后端实现
tauri分支：app管理通过rust实现(废弃，迁到https://gitee.com/liji1211/tauri-vue3-appscheduler)

### 软件架构
后端采用fastapi + sqlalchemy + MySql
前端基于开源项目[pure-admin-thin](https://github.com/pure-admin/pure-admin-thin)
桌面端使用tauri来实现

### 使用说明
#### 运行web项目
切换到web分支，查看README.md

#### 运行桌面客户端
切换到tauri分支，查看README.md
