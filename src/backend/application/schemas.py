from typing import Optional

from pydantic.networks import HttpUrl

from ..core.schemas import Pagination, MyBaseModel, NameStr, PrimaryKey
from ..application_category.schemas import ApplicationCategoryCreate, ApplicationCategoryRead


class ApplicationBase(MyBaseModel):
    name: NameStr
    status: str
    banner: Optional[HttpUrl] = None
    description: Optional[str] = None


class ApplicationCreate(ApplicationBase):
    category: Optional[ApplicationCategoryCreate] = None


class ApplicationRead(ApplicationBase):
    id: PrimaryKey
    category: Optional[ApplicationCategoryRead] = None


class ApplicationPagination(Pagination):
    data: list[ApplicationRead]
