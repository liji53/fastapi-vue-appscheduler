from typing import Optional
from datetime import datetime

from ..core.schemas import MyBaseModel, NameStr, PrimaryKey
from ..core.schemas import Pagination


class ProjectBase(MyBaseModel):
    name: NameStr
    remark: Optional[str] = None


class ProjectCreate(ProjectBase):
    pass


class ProjectUpdate(ProjectBase):
    pass


class ProjectRead(ProjectBase):
    id: PrimaryKey
    task_count: int
    running_count: int
    failed_count: int
    created_at: datetime


class ProjectPagination(Pagination):
    data: list[ProjectRead] = []
