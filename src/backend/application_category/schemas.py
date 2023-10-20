from typing import Optional

from ..core.schemas import MyBaseModel, NameStr, PrimaryKey
from ..core.schemas import Pagination


class ApplicationCategoryBase(MyBaseModel):
    name: NameStr
    description: Optional[str] = None


class ApplicationCategoryCreate(ApplicationCategoryBase):
    pass


class ApplicationCategoryRead(ApplicationCategoryBase):
    id: PrimaryKey


class ApplicationCategoryPagination(Pagination):
    data: list[ApplicationCategoryRead] = []
