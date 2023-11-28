import psutil
from fastapi import APIRouter

from .schemas import SysResource


sys_resource_router = APIRouter()


@sys_resource_router.get("", response_model=SysResource, summary="获取系统资源的使用情况（cpu、内存、磁盘）")
def get_sys_resource():
    usage = psutil.disk_usage("/")
    return {
        "cpu": psutil.cpu_percent(interval=1),
        "memory": psutil.virtual_memory().percent,
        "disk": int(usage.used / (1024*1024*1024)),
        "full_disk": int(usage.total / (1024*1024*1024))
    }
