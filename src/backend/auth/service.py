from typing import Optional, Annotated, Union

from fastapi import Depends, Request, HTTPException
from fastapi.security.utils import get_authorization_scheme_param
from loguru import logger
from jose import jwt

from .models import User
from .schemas import UserCreate, UserUpdate, UserPasswdReset, UserStatusUpdate

from ..core.config import JWT_SECRET, JWT_ALG
from ..permission.models import Role

UNAUTHORIZED_EXCEPTION = HTTPException(status_code=401, detail=[{"msg": "未认证."}])


def get_by_name(*, db_session, username: str) -> Optional[User]:
    return db_session.query(User).filter(User.username == username).one_or_none()


def get_by_id(*, db_session, user_id) -> Optional[User]:
    return db_session.query(User).filter(User.id == user_id).one_or_none()


def create(*, db_session, user_in: UserCreate) -> User:
    """创建用户"""
    if user_in.roles:
        user = User(**user_in.model_dump())
    else:
        user = User(**user_in.model_dump(exclude=["roles"]))

    db_session.add(user)
    db_session.commit()
    return user


def update(*, db_session, user: User, user_in: Union[UserUpdate, UserPasswdReset, UserStatusUpdate]):
    """更新用户信息"""
    user_data = user.dict()
    update_data = user_in.model_dump()

    for field in user_data:
        if field in update_data:
            setattr(user, field, update_data[field])

    db_session.commit()
    return user


def delete(*, db_session, user_ids: list[int]):
    db_session.query(User).filter(User.id.in_(user_ids)).delete()
    db_session.commit()


def get_current_user(request: Request) -> User:
    """基于token获取当前登录的用户"""
    authorization: str = request.headers.get("Authorization")
    if not authorization:
        logger.error("authorization不存在")
        raise UNAUTHORIZED_EXCEPTION

    scheme, param = get_authorization_scheme_param(authorization)
    if scheme.lower() != "bearer":
        logger.error("authorization非法")
        raise UNAUTHORIZED_EXCEPTION

    token = authorization.split()[1]

    try:
        data = jwt.decode(token, JWT_SECRET, algorithms=JWT_ALG)
    except:
        logger.error("jwt 解码失败.")
        raise UNAUTHORIZED_EXCEPTION

    if not data.__contains__("username") or not data["username"]:
        logger.error("token 中不存在username信息")
        raise UNAUTHORIZED_EXCEPTION

    return get_by_name(db_session=request.state.db, username=data["username"])


def get_current_roles(current_user: User = Depends(get_current_user)) -> list[Role]:
    return current_user.roles


# 当前登录的用户
CurrentUser = Annotated[User, Depends(get_current_user)]
# 当前用户的角色
CurrentRoles = Annotated[list[Role], Depends(get_current_roles)]
