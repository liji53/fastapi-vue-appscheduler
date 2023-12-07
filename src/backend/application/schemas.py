from typing import Optional

from pydantic.networks import HttpUrl

from ..core.schemas import Pagination, MyBaseModel, NameStr, PrimaryKey


class ApplicationBase(MyBaseModel):
    name: NameStr
    url: HttpUrl
    category_id: PrimaryKey
    status: bool = True
    description: Optional[str] = None


class ApplicationCreate(ApplicationBase):
    pass


class ApplicationUpdate(ApplicationBase):
    name: Optional[NameStr] = None
    url: Optional[HttpUrl] = None
    category_id: Optional[PrimaryKey] = None


class ApplicationRead(ApplicationBase):
    id: PrimaryKey
    banner: Optional[str] = None
    is_installed: bool = False


class ApplicationPagination(Pagination):
    data: list[ApplicationRead]


class AppTreeNode(MyBaseModel):
    id: int
    name: NameStr
    children: Optional[list['AppTreeNode']] = None


class AppTree(MyBaseModel):
    data: list[AppTreeNode]


class AppReadme(MyBaseModel):
    data: str
