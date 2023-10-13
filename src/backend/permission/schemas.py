from typing import Optional, Union

from .models import Menu

from ..core.schemas import MyBaseModel


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


class RoleRegister(MyBaseModel):
    name: str
    code: str
    is_active: bool = True
    description: Optional[str] = None
    menus: list[Union[Menu, int]] = []






