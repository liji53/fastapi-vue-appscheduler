# docker 镜像打包

### 后端镜像制作
在2G内存的雲服務器上，會打包失敗
```
docker build -t appscheduler -f docker/dockerfile .
```


### 启动服务
```
docker-compose -f docker/docker-compose.yml up -d
```

