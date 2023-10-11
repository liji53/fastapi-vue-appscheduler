from sqlalchemy import Column, String, Integer, ForeignKey, Boolean, Table
from sqlalchemy.orm import relationship

from ..core.database import Base
from ..core.models import DateTimeMixin


# 中间表, 创建后，不需要维护
roles_menus = Table(
    'roles_menus',
    Base.metadata,
    Column("id", Integer, primary_key=True),
    Column('role_id', Integer, ForeignKey('role.id')),
    Column('menu_id', Integer, ForeignKey('menu.id'))
)


class MenuMeta(Base, DateTimeMixin):
    id = Column(Integer, primary_key=True)
    title = Column(String(128), nullable=False, comment="菜单名称")
    icon = Column(String(128), comment="菜单图标")
    rank = Column(Integer, comment="菜单排序，值越高排的越后（只针对顶级路由）")
    show_link = Column(Boolean, comment="是否显示菜单")

    menu_id = Column(Integer, ForeignKey('menu.id'))


class Menu(Base, DateTimeMixin):
    id = Column(Integer, primary_key=True)
    parent_id = Column(Integer, ForeignKey('menu.id'))
    children = relationship("Menu", backref='parent', remote_side=[id])

    path = Column(String(256), nullable=False, comment="路由地址")
    name = Column(String(128), unique=True, comment="路由名称(需与组件名称一致)")
    meta = relationship("MenuMeta", uselist=False)  # 1对1的关系

    roles = relationship("Role", secondary=roles_menus, backref="menu")


class Role(Base, DateTimeMixin):
    id = Column(Integer, primary_key=True)
    name = Column(String(128), unique=True, nullable=False, comment="角色名称")
    is_active = Column(Boolean, default=True, comment="是否启用")

    menus = relationship("Menu", secondary=roles_menus, backref="role")
