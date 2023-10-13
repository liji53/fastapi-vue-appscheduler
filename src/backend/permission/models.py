from sqlalchemy import Column, String, Integer, ForeignKey, Boolean, Table
from sqlalchemy.orm import relationship

from ..auth.models import UserRole
from ..core.database import Base
from ..core.models import DateTimeMixin


RoleMenu = Table(
    'roles_menus',
    Base.metadata,
    Column('role_id', Integer, ForeignKey("role.id")),
    Column('menu_id', Integer, ForeignKey("menu.id"))
)


class Role(Base, DateTimeMixin):
    id = Column(Integer, primary_key=True)
    name = Column(String(128), nullable=False, comment="角色名称")
    code = Column(String(128), unique=True, nullable=False, comment="角色标识")
    is_active = Column(Boolean, default=True, comment="是否启用")
    description = Column(String(512), comment="备注")

    users = relationship("User", secondary=UserRole, back_populates="roles")
    menus = relationship("Menu", secondary=RoleMenu, back_populates="roles")  # 只关联叶子节点

    def __repr__(self) -> str:
        return f"<{self.code}>"


class Menu(Base, DateTimeMixin):
    id = Column(Integer, primary_key=True)
    path = Column(String(256), nullable=False, comment="路由地址(需与组件路径一致)")  # 必须与web/src/views目录的的路径一致
    name = Column(String(128), comment="路由名称(需与组件名称一致)")
    meta = relationship("MenuMeta", uselist=False)  # 1对1的关系

    parent_id = Column(Integer, ForeignKey('menu.id'))
    parent = relationship("Menu", remote_side=[id], backref="children")  # 父菜单可以有多个子菜单，一个子菜单只能有一个父菜单

    roles = relationship("Role", secondary=RoleMenu, back_populates="menus")


class MenuMeta(Base, DateTimeMixin):
    id = Column(Integer, primary_key=True)
    title = Column(String(128), nullable=False, comment="菜单名称")
    icon = Column(String(128), comment="菜单图标")
    rank = Column(Integer, comment="菜单排序，值越高排的越后（只针对顶级路由）")
    show_link = Column(Boolean, default=True, comment="是否显示菜单")

    menu_id = Column(Integer, ForeignKey(Menu.id))

