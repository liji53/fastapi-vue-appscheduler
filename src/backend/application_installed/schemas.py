from typing import Optional

from ..core.schemas import Pagination, MyBaseModel, NameStr, PrimaryKey


class InstalledApp(MyBaseModel):
    name: NameStr
    description: Optional[str] = None


class InstalledAppCreate(MyBaseModel):
    app_id: int


class InstalledAppUpdate(InstalledApp):
    pass


class InstalledAppRead(InstalledApp):
    id: PrimaryKey
    banner: Optional[str] = None
    is_online: bool = False
    category_id: Optional[int] = None
    version: Optional[str] = None


class InstalledAppPagination(Pagination):
    data: list[InstalledAppRead]


class InstalledAppTreeNode(MyBaseModel):
    id: int
    name: NameStr
    children: list['InstalledAppTreeNode']


class InstalledAppTree(MyBaseModel):
    data: list[InstalledAppTreeNode]
