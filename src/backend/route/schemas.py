from typing import Optional

from ..core.schemas import MyBaseModel


class MenuMeta(MyBaseModel):
    title: str
    icon: Optional[str]
    rank: Optional[int]
    roles: Optional[list[str]]
    auths: Optional[list[str]]


class MenuItem(MyBaseModel):
    path: str
    name: Optional[str]
    meta: MenuMeta
    children: Optional[list['MenuItem']]   # 模型可能还没有被解析出来，所以使用字符串


class RouteResponse(MyBaseModel):
    data: list[MenuItem]
