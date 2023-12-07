from typing import Optional
from datetime import datetime

from ..core.schemas import MyBaseModel, NameStr, PrimaryKey
from ..core.schemas import Pagination


class ApplicationCategoryBase(MyBaseModel):
    name: NameStr
    description: Optional[str] = None


class ApplicationCategoryCreate(ApplicationCategoryBase):
    pass


class ApplicationCategoryUpdate(ApplicationCategoryBase):
    pass


class ApplicationCategoryRead(ApplicationCategoryBase):
    id: PrimaryKey
    app_count: int
    installed_app_count: int
    installed_sum_count: int
    created_at: datetime


class ApplicationCategoryPagination(Pagination):
    data: list[ApplicationCategoryRead] = []
