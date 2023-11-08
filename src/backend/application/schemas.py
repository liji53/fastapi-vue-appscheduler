from typing import Optional

from pydantic.networks import HttpUrl

from ..core.schemas import Pagination, MyBaseModel, NameStr, PrimaryKey


class ApplicationBase(MyBaseModel):
    name: NameStr
    url: HttpUrl
    status: bool = True
    category_id: Optional[PrimaryKey] = None
    banner: Optional[str] = None
    description: Optional[str] = None


class ApplicationCreate(ApplicationBase):
    pass


class ApplicationUpdate(ApplicationBase):
    pass


class AppStatusUpdate(MyBaseModel):
    status: bool


class ApplicationRead(ApplicationBase):
    id: PrimaryKey
    is_installed: bool = False


class ApplicationPagination(Pagination):
    data: list[ApplicationRead]
