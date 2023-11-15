from typing import Optional
from datetime import datetime

from ..core.schemas import MyBaseModel, NameStr, PrimaryKey
from ..core.schemas import Pagination


class TaskBase(MyBaseModel):
    name: NameStr
    project_id: PrimaryKey
    app_id: PrimaryKey
    remark: Optional[str] = None


class TaskCreate(TaskBase):
    status: bool = True
    pass


class TaskUpdate(TaskBase):
    pass


class TaskStatusUpdate(MyBaseModel):
    status: bool


class TaskCronUpdate(MyBaseModel):
    cron: str


class TaskRead(TaskBase):
    id: PrimaryKey
    project: str
    status: bool
    cron: Optional[str] = None
    updated_at: datetime


class TaskPagination(Pagination):
    data: list[TaskRead] = []
