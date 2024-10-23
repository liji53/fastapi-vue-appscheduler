# 介绍
支持app管理 + app调度(定时、手动), 这里app 指的是具有指定结构的python项目。
安装app时，会自动根据项目地址(目前仅支持svn)下载python项目，然后基于requirements.txt 安装依赖。

## 功能演示
在线demo: http://60.204.224.115:8000

用户名: admin, 密码：admin123

#### 项目截图
待完善

## 部署
#### 下载源码
```shell
git clone https://gitee.com/liji1211 fastapi-vue-appscheduler.git
cd fastapi-vue-appscheduler
```
#### 使用docker-compose部署
如果服务器内存(2G)太小，web会编译失败
```shell
docker-compose -f docker/docker-compose.yml up -d
```

## 软件架构
后端采用fastapi + sqlalchemy + MySql
前端基于开源项目[pure-admin-thin](https://github.com/pure-admin/pure-admin-thin)
桌面端使用tauri来实现

## 开发
待补充