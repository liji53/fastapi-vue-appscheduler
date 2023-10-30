from typing import Union, Annotated
import time
import uuid
import os

from fastapi import APIRouter, HTTPException, Query, File
from loguru import logger
from sqlalchemy.exc import IntegrityError

from .schemas import UserLogin, UserLoginResponse, UserRead, UserCreate, UserUpdate, UserPagination, \
    UserPasswdReset, UserStatusUpdate, UserBatchDelete, UserRolesRead, UserRolesUpdate
from .service import get_by_name, create, get_by_id, update, delete

from ..core.database import DbSession
from ..core.service import CurrentUser, CommonParameters, sort_paginate
from ..core.schemas import PrimaryKey
from ..core.config import FILES_DIR, FILES_DIR_NAME

auth_router = APIRouter()
user_router = APIRouter()

NOT_FOUND_EXCEPTION = HTTPException(404, detail=[{"msg": "该用户不存在！"}])


@auth_router.post("/login", response_model=UserLoginResponse, summary="登录")
def login(user_in: UserLogin, db_session: DbSession):
    logger.debug(f"登录: {user_in.model_dump()}")
    user = get_by_name(db_session=db_session, username=user_in.username)
    if user and user.check_password(user_in.password):
        return {"username": user.username, "avatar": user.avatar, "roles": ["admin"],
                "accessToken": user.token, "refreshToken": "?", "expires": user.expired}

    raise HTTPException(status_code=422, detail=[{"msg": "登录失败!"}])


@user_router.get("", response_model=UserPagination, summary="获取用户列表")
def get_users(common: CommonParameters, username: str = "", phone: str = "",
              active: str = Query(default="", alias="status")):
    """获取用户列表"""
    # todo: 权限控制
    filter_spec = []
    if username:
        filter_spec.append({"field": "username", 'op': 'like', 'value': f"%{username}%"})
    if phone:
        filter_spec.append({"field": "phone", 'op': '==', 'value': phone})
    if active:
        filter_spec.append({"field": "status", 'op': '==', 'value': True if active == "true" else False})

    return sort_paginate(model="User", filter_spec=filter_spec, **common)


@user_router.post("", response_model=UserRead, summary="新建用户")
def create_user(user_in: UserCreate, db_session: DbSession, current_user: CurrentUser):
    """创建新用户"""
    # todo: 权限控制
    user = get_by_name(db_session=db_session, username=user_in.username)
    if user:
        logger.warning(f"创建用户失败，原因：用户{user.username}已经存在")
        raise HTTPException(422, detail=[{"msg": "该用户已经存在!"}])
    try:
        user = create(db_session=db_session, user_in=user_in)
    except IntegrityError:
        raise HTTPException(422, detail=[{"msg": "用户名/手机号/邮箱 已经存在了"}])
    return user


@user_router.put("/{user_id}", response_model=UserRead, summary="更新用户信息, 更新用户状态, 重置密码")
def update_user(user_id: PrimaryKey, user_in: Union[UserUpdate, UserStatusUpdate, UserPasswdReset, UserRolesUpdate],
                db_session: DbSession, current_user: CurrentUser):
    """更新用户"""
    # todo: 权限控制
    user = get_by_id(db_session=db_session, user_id=user_id)
    if not user:
        raise NOT_FOUND_EXCEPTION

    user = update(db_session=db_session, user=user, user_in=user_in)
    return user


@user_router.delete("/{user_id}", response_model=None, summary="删除用户")
def delete_user(user_id: PrimaryKey, db_session: DbSession, current_user: CurrentUser):
    """删除新用户"""
    # todo: 权限控制
    try:
        delete(db_session=db_session, user_ids=[user_id])
    except Exception as e:
        logger.debug(f"删除用户{user_id}失败，原因: {e}")
        raise HTTPException(500, detail=[{"msg": f"用户{user_id}不能被删除，请确保该用户没有关联的应用"}])


@user_router.delete("", response_model=None, summary="删除用户")
def batch_delete(db_session: DbSession, ids_in: UserBatchDelete, current_user: CurrentUser):
    """批量删除用户"""
    try:
        delete(db_session=db_session, user_ids=ids_in.ids)
    except Exception as e:
        logger.debug(f"删除用户{ids_in.ids}失败，原因: {e}")
        raise HTTPException(500, detail=[{"msg": f"用户{ids_in.ids}不能被删除，请确保该用户没有关联的应用"}])


@user_router.post("/{user_id}/avatar", response_model=None, summary="上传用户头像")
def upload_file(user_id: PrimaryKey, file: Annotated[bytes, File(alias="blob")], db_session: DbSession):
    """上传文件，前端数据通过blob字段传递，而不是file
    采用本地存储临时方案
    todo: 限制上传的文件大小
    """
    user = get_by_id(db_session=db_session, user_id=user_id)
    if not user:
        raise NOT_FOUND_EXCEPTION
    old_file_path = os.path.join(FILES_DIR, user.avatar.replace(FILES_DIR_NAME, "")[1:])
    logger.debug(f"删除旧头像文件路径：{old_file_path}")
    if os.path.exists(old_file_path):
        os.remove(old_file_path)

    file_name = f"{str(uuid.uuid4())}.png"
    url_dir = time.strftime(f"avatar/{user_id}/%Y-%m-%d/")
    save_dir = os.path.join(FILES_DIR, url_dir)

    if not os.path.exists(save_dir):
        os.makedirs(save_dir)

    with open(os.path.join(save_dir, file_name), 'wb') as fd:
        fd.write(file)

    update(db_session=db_session, user=user, user_in={"avatar": os.path.join(FILES_DIR_NAME, url_dir, file_name)})


@user_router.get("/{user_id}/roles", response_model=UserRolesRead, summary="获取用户的角色")
def get_user_roles(user_id: PrimaryKey, db_session: DbSession):
    user = get_by_id(db_session=db_session, user_id=user_id)
    return {"data": [role.id for role in user.roles]}
