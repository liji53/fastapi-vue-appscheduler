from datetime import datetime

from ..core.schemas import MyBaseModel, PrimaryKey
from ..core.schemas import Pagination
from .models import SeverityEnum


class LogBase(MyBaseModel):
    status: bool
    execute_type: str


class LogCreate(LogBase):
    task_id: PrimaryKey
    content: str


class LogContentRead(MyBaseModel):
    data: str


class LogRead(LogBase):
    id: PrimaryKey
    log_type: SeverityEnum
    created_at: datetime
    project_name: str
    task_name: str


class LogPagination(Pagination):
    data: list[LogRead] = []


class LogRecently(LogBase):
    id: PrimaryKey
    log_type: SeverityEnum
    created_at: datetime
    content: str
