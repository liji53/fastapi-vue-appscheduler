from typing import Optional
from datetime import datetime

from fastapi import HTTPException
from croniter import croniter
from pydantic import field_validator

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
    cron: Optional[str]

    @field_validator("cron")
    @classmethod
    def ensure_foobar(cls, v: Optional[str]):
        if v and not croniter.is_valid(expression=v):
            # 不能使用 raise ValueError("xxx")
            raise HTTPException(422, detail=[{"msg": "cron表达式非法！"}])
        return v


class TaskRead(TaskBase):
    id: PrimaryKey
    app_id: PrimaryKey
    project: str
    status: bool
    cron: Optional[str] = None
    next_at: Optional[str] = None
    updated_at: datetime
    url: str


class TaskPagination(Pagination):
    data: list[TaskRead] = []


class TaskConfigRead(MyBaseModel):
    data: Optional[str] = None


class TaskConfigUpdate(TaskConfigRead):
    pass


class TaskTreeNode(MyBaseModel):
    id: Optional[int] = None
    name: NameStr
    children: Optional[list['TaskTreeNode']] = None


class TaskTree(MyBaseModel):
    data: list[TaskTreeNode]