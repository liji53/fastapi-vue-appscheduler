from typing import Optional, Annotated

from fastapi import Depends, Request, HTTPException
from fastapi.security.utils import get_authorization_scheme_param
from loguru import logger
from jose import jwt

from .models import User
from .schemas import UserRegister

from ..core.config import JWT_SECRET, JWT_ALG
from ..permission.models import Role

UNAUTHORIZED_EXCEPTION = HTTPException(status_code=401, detail="未认证.")


def get_user_by_name(*, db_session, username: str) -> Optional[User]:
    return db_session.query(User).filter(User.username == username).one_or_none()


def create_user(*, db_session, user_in: UserRegister) -> User:
    """创建用户"""
    user = User(**user_in.model_dump())

    db_session.add(user)
    db_session.commit()
    return user


def get_current_user(request: Request) -> User:
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

    return get_user_by_name(db_session=request.state.db, username=data["username"])


def get_current_roles(current_user: User = Depends(get_current_user)) -> list[Role]:
    return current_user.roles


# 当前登录的用户
CurrentUser = Annotated[User, Depends(get_current_user)]
# 当前用户的角色
CurrentRoles = Annotated[list[Role], Depends(get_current_roles)]
