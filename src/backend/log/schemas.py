from datetime import datetime

from ..core.schemas import MyBaseModel, PrimaryKey
from ..core.schemas import Pagination
from .models import SeverityEnum


class LogRead(MyBaseModel):
    id: PrimaryKey
    project_name: str
    task_name: str
    status: bool
    log_type: SeverityEnum
    execute_type: str
    created_at: datetime


class LogContentRead(MyBaseModel):
    data: str


class LogPagination(Pagination):
    data: list[LogRead] = []
