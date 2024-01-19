# fastapi-vue-appscheduler

### 介绍
app 管理 + app 调度, app 指的是python项目。
安装app时，会自动根据项目地址(目前仅支持svn)下载python项目，然后基于requirements.txt 安装依赖。

### 软件架构
后端采用fastapi + sqlalchemy + MySql
前端基于开源项目[pure-admin-thin](https://github.com/pure-admin/pure-admin-thin)

### 使用说明
#### 运行项目
##### windows运行
如果应用的项目仓库在svn上，则依赖svn命令行工具
下载地址：https://www.visualsvn.com/downloads/
下载之后解压，把bin目录加入到环境变量中。

前端打包：参考<https://yiming_chang.gitee.io/pure-admin-doc/pages/request/#%E5%9F%BA%E7%A1%80%E7%94%A8%E6%B3%95>

##### docker运行
```shell
docker-compose -f docker/docker-compose.yml up -d
```

##### 打包成桌面应用
打包成release
```shell
cargo tauri build
```
打包debug
```shell
cargo tauri dev
```
