from typing import Optional, Union
from datetime import datetime

from .models import Menu

from ..core.schemas import MyBaseModel, Pagination, PrimaryKey, NameStr


class MenuMeta(MyBaseModel):
    title: str
    icon: Optional[str] = None
    rank: Optional[int] = None
    keepAlive: bool = False
    roles: Optional[list[str]] = None
    auths: list[str] = []


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


class RoleUpdate(MyBaseModel):
    name: NameStr
    code: NameStr
    remark: Optional[str] = None


class RoleStatusUpdate(MyBaseModel):
    status: bool


class RoleMenuItem(MyBaseModel):
    id: PrimaryKey
    title: str
    children: Optional[list['RoleMenuItem']] = None


class RoleMenuUpdate(MyBaseModel):
    menus: list[PrimaryKey]  # 叶子节点的id


class RoleMenuRead(MyBaseModel):
    menus: list[RoleMenuItem]
    activedMenus: list[PrimaryKey]


class RoleRead(RoleBase):
    id: PrimaryKey
    created_at: datetime


class RolePagination(Pagination):
    data: list[RoleRead]
