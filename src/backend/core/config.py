from starlette.config import Config
from loguru import logger
import os

config = Config(".env")

# 日志等级
LOG_LEVEL = config("LOG_LEVEL", default="WARNING")

# web 文件路径
DEFAULT_STATIC_DIR = os.path.join(
    os.path.abspath(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))), os.path.join("frontend", "dist")
)
STATIC_DIR = config("STATIC_DIR", default=DEFAULT_STATIC_DIR)
logger.debug(f"默认web路径：{STATIC_DIR}")

# 数据库
DATABASE_HOSTNAME = config("DATABASE_HOSTNAME")
DATABASE_NAME = config("DATABASE_NAME", default="appscheduler")
DATABASE_PORT = config("DATABASE_PORT", default="3306")
DATABASE_USER = config("DATABASE_USER", default="hs_app_scheduler")
DATABASE_PASSWORD = config("DATABASE_PASSWORD", default="123456")
DATABASE_ENGINE_POOL_SIZE = config("DATABASE_ENGINE_POOL_SIZE", cast=int, default=20)
DATABASE_ENGINE_MAX_OVERFLOW = config("DATABASE_ENGINE_MAX_OVERFLOW", cast=int, default=0)
DATABASE_URI = f"mysql+pymysql://{DATABASE_USER}:{DATABASE_PASSWORD}@{DATABASE_HOSTNAME}:{DATABASE_PORT}/{DATABASE_NAME}"
logger.debug(f"数据库连接地址：{DATABASE_URI}")

# 认证
JWT_SECRET = config("JWT_SECRET", default="develop")
JWT_ALG = config("JWT_ALG", default="HS256")
JWT_EXP = config("JWT_EXP", cast=int, default=24*60*60)   # Seconds
