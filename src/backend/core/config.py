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

# 本地存储文件路径 - 上传的图片
FILES_DIR_NAME = "files"
DEFAULT_FILES_DIR = os.path.join(
    os.path.abspath(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))), FILES_DIR_NAME
)
FILES_DIR = config("FILES_DIR", default=DEFAULT_FILES_DIR)
logger.debug(f"默认file路径: {FILES_DIR}")

# 认证
JWT_SECRET = config("JWT_SECRET", default="develop")
JWT_ALG = config("JWT_ALG", default="HS256")
JWT_EXP = config("JWT_EXP", cast=int, default=2*60*60)   # 2小时过期
JWT_REFRESH_TOKEN_EXP = config("JWT_REFRESH_TOKEN_EXP", cast=int, default=7*24*60*60)  # 7天过期

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

# 数据库迁移 配置文件路径
ALEMBIC_INI_PATH = config(
    "ALEMBIC_INI_PATH",
    default=os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), "alembic.ini"),
)

# 如果安装的是svn项目，需要用到的svn账户、密码
SVN_USER = config("SVN_USER", default="liji37951")
SVN_PASSWORD = config("SVN_PASSWORD", default="???")

# 安装时, 会下载requirements.txt的python包，需要pip源
PIP_INDEX_URL = config("PIP_INDEX_URL", default="https://mirrors.aliyun.com/pypi/simple/")

# 解析日志时，要用到的错误、警告的日志格式
LOG_ERROR_PATTERN = config("LOG_ERROR_PATTERN", default=r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\.\d{3} \| ERROR')
LOG_WARNING_PATTERN = config("LOG_WARNING_PATTERN", default=r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\.\d{3} \| WARNING')
