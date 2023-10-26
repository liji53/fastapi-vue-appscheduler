from typing import Optional, Union
from datetime import datetime

from .models import Menu

from ..core.schemas import MyBaseModel, Pagination, PrimaryKey, NameStr


class MenuMeta(MyBaseModel):
    title: str
    icon: Optional[str] = None
    rank: Optional[int] = None
    roles: Optional[list[str]] = None
    auths: Optional[list[str]] = None


class MenuItem(MyBaseModel):
    path: str
    name: Optional[str] = None
    meta: MenuMeta
    children: Optional[list['MenuItem']] = None   # 模型还没有被解析出来，所以使用字符串


class RouteResponse(MyBaseModel):
    data: list[MenuItem]


class RoleBase(MyBaseModel):
    name: NameStr
    code: NameStr
    status: bool = True
    remark: Optional[str] = None


class RoleCreate(RoleBase):
    menus: Optional[list[Union[PrimaryKey, Menu]]] = None


class RoleRead(RoleBase):
    id: PrimaryKey
    created_at: datetime
    updated_at: datetime


class RolePagination(Pagination):
    data: list[RoleRead]
