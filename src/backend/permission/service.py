from typing import Optional

from loguru import logger

from .models import Role, Menu
from .schemas import RoleRegister


def get_menus_by_roles(*, db_session, roles: list[Role]) -> list[Menu]:
    for role in roles:
        print(role.name)
    return []


def get_role_by_name(*, db_session, name: str) -> Optional[Role]:
    return db_session.query(Role).filter(Role.name == name).one_or_none()


def get_roles(*, db_session, role_ids: list[int]) -> list[Role]:
    logger.debug("")
    return db_session.query(Role).filter(Role.id.in_(role_ids)).all()


def create_role(*, db_session, role_in: RoleRegister) -> Role:
    role = Role(**role_in.model_dump())
    # role.menus = []
    db_session.add(role)
    db_session.commit()
    return role
