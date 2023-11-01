from typing import Optional, Union

from loguru import logger

from .models import Role, Menu, MenuMeta
from .schemas import RoleCreate, RoleUpdate, MenuItem, RoleStatusUpdate, RoleMenuUpdate


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


def update(*, db_session, role: Role, role_in: Union[RoleUpdate, RoleStatusUpdate, RoleMenuUpdate]) -> Role:
    role_data = role.dict()
    update_data = role_in.model_dump()

    for field in role_data:
        if field in update_data:
            setattr(role, field, update_data[field])

    if update_data.__contains__("menus"):
        logger.info(f"更新角色的菜单：叶子节点的ids为：{update_data['menus']}")
        menus = get_menus_by_ids(db_session=db_session, ids=update_data['menus'])
        if menus:
            role.menus = menus
        else:
            logger.warning("不存在这些menus")

    db_session.commit()
    return role


def delete(*, db_session, role_id: int):
    db_session.query(Role).filter(Role.id == role_id).delete()
    db_session.commit()


def get_menus(*, db_session) -> Optional[list[Menu]]:
    return db_session.query(Menu).all()


def get_menus_by_ids(*, db_session, ids: list[int]) -> Optional[list[Menu]]:
    return db_session.query(Menu).filter(Menu.id.in_(ids)).all()


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
