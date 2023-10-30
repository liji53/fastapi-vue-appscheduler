import sys
import os

from fastapi import FastAPI
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from loguru import logger

from .core.config import LOG_LEVEL, STATIC_DIR, FILES_DIR, FILES_DIR_NAME
from .core.api import api_router
from .core.middleware import DBSessionMiddleware

# 配置日志等级
logger.remove()
logger.add(sys.stderr, level=LOG_LEVEL)


# app-scheduler应用
app = FastAPI(openapi_url="")


# api的异常处理
async def not_found(request, exc):
    return JSONResponse(
        status_code=404, content={"detail": [{"msg": "API不支持."}]}
    )


async def internal_error(request, exc):
    return JSONResponse(
        status_code=500, content={"detail": [{"msg": "API服务内部错误."}]}
    )
exception_handlers = {404: not_found, 500: internal_error}   # 404异常的处理

# 后端api
api = FastAPI(
    exception_handlers=exception_handlers,
    title="App Scheduler",
    description="App Scheduler's API documentation.",
    root_path="/api/v1",
)
# 添加中间件
api.add_middleware(DBSessionMiddleware)
# 添加所有的API路由
api.include_router(api_router)

# 前端路由
frontend = FastAPI(openapi_url="")


@frontend.middleware("http")
async def default_page(request, call_next):
    response = await call_next(request)
    if response.status_code == 404:
        if STATIC_DIR:
            return FileResponse(os.path.join(STATIC_DIR, "index.html"))
    return response

if STATIC_DIR and os.path.isdir(STATIC_DIR):
    frontend.mount("/", StaticFiles(directory=STATIC_DIR), name="app")

# 上传图片的路由
files = FastAPI(openapi_url="")
if FILES_DIR:
    if not os.path.exists(FILES_DIR):
        os.makedirs(FILES_DIR)
    files.mount(f"", StaticFiles(directory=FILES_DIR), name="file")

# 挂载前端、后端api、存储系统
app.mount("/api/v1", app=api)
app.mount(f"/{FILES_DIR_NAME}", app=files)
app.mount("/", app=frontend)

