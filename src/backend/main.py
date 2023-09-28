import sys
import os

from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from loguru import logger

from .core.config import LOG_LEVEL, STATIC_DIR
from .core.api import api_router
from .core.middleware import DBSessionMiddleware

# 配置日志等级
logger.remove()
logger.add(sys.stderr, level=LOG_LEVEL)

# app-scheduler应用
app = FastAPI(openapi_url="")

# 后端api
api = FastAPI(
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

# 挂载前端和后端api
app.mount("/api/v1", app=api)
app.mount("/", app=frontend)