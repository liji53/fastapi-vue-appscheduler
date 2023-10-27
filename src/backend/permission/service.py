from typing import Optional, Union

from .models import Role, Menu, MenuMeta
from .schemas import RoleCreate, RoleUpdate, MenuItem, RoleStatusUpdate


def get_by_code(*, db_session, code: str) -> Optional[Role]:
    return db_session.query(Role).filter(Role.code == code).one_or_none()


def get_by_id(*, db_session, role_id: int) -> Optional[Role]:
    return db_session.query(Role).filter(Role.id == role_id).one_or_none()


def get_roles(*, db_session, role_ids: list[int]) -> Optional[list[Role]]:
    return db_session.query(Role).filter(Role.id.in_(role_ids)).all()


def create(*, db_session, role_in: RoleCreate) -> Role:
    if role_in.menus:
        role = Role(**role_in.model_dump())
    else:
        role = Role(**role_in.model_dump(exclude=["menus"]))

    db_session.add(role)
    db_session.commit()
    return role


def update(*, db_session, role: Role, role_in: Union[RoleUpdate, RoleStatusUpdate]) -> Role:
    role_data = role.dict()
    update_data = role_in.model_dump()

    for field in role_data:
        if field in update_data:
            setattr(role, field, update_data[field])

    db_session.commit()
    return role


def delete(*, db_session, role_id: int):
    db_session.query(Role).filter(Role.id == role_id).delete()
    db_session.commit()


def get_menus(*, db_session) -> Optional[list[Menu]]:
    return db_session.query(Menu).all()


# todo: 支持任意层级的菜单目录
def create_menus(*, db_session, menu_in: MenuItem) -> list[Menu]:
    """return: 返回叶子节点"""
    ret = []
    parent_menu = Menu(
        **menu_in.model_dump(exclude=["meta", "children"]),
        meta=MenuMeta(**menu_in.meta.model_dump(exclude=["roles", "auths"])),
    )
    db_session.add(parent_menu)

    if menu_in.children:
        for child_menu in menu_in.children:
            sub_menu = Menu(
                **child_menu.model_dump(exclude=["meta", "children"]),
                meta=MenuMeta(**child_menu.meta.model_dump(exclude=["roles", "auths"]))
            )
            sub_menu.parent = parent_menu
            db_session.add(sub_menu)
            ret.append(sub_menu)
    else:
        ret.append(parent_menu)

    db_session.commit()
    return ret
