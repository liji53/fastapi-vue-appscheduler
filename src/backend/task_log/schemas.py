from datetime import datetime

from ..core.schemas import MyBaseModel, PrimaryKey
from ..core.schemas import Pagination
from .models import SeverityEnum


class LogBase(MyBaseModel):
    id: PrimaryKey
    status: bool
    log_type: SeverityEnum
    execute_type: str
    created_at: datetime


class LogContentRead(MyBaseModel):
    data: str


class LogRead(LogBase):
    project_name: str
    task_name: str


class LogPagination(Pagination):
    data: list[LogRead] = []


class LogRecently(LogBase):
    content: str
