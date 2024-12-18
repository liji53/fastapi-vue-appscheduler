from typing import Optional, Annotated
import asyncio

from fastapi import APIRouter, HTTPException, File
from loguru import logger

from .service import get_by_id, create, update, delete
from .schemas import InstalledAppCreate, InstalledAppPagination, InstalledAppUpdate, \
    InstalledAppRead, InstalledAppTree, InstalledAppReadme

from ..application import service as app_service
from ..task.models import Task
from ..core.service import CommonParameters, sort_paginate, DbSession, CurrentUser
from ..core.schemas import PrimaryKey
from ..core.database import SessionLocal
from ..utils.storage import remove_old_file, create_new_file, remove_dir
from ..utils.repository import Svn

installed_app_router = APIRouter()
STORAGE_MY_APP_DIR = "my_apps"  # 存储应用的logo图片


def task_is_online(task: Task):
    return task.cron and task.status


@installed_app_router.get("", response_model=InstalledAppPagination, summary="获取我的应用列表")
def get_installed_apps(
        common: CommonParameters,
        category_id: Optional[int] = None,
        is_online: Optional[bool] = None
):
    pagination = sort_paginate(model="ApplicationInstalled", **common)
    ret = {
        'data': [{
            **app.dict(),
            "category_id": app.application.category_id,
            "is_online": any(task_is_online(task) for task in app.tasks)
        } for app in pagination["data"]
            if (category_id is None or category_id == app.application.category_id) and
               (is_online is None or is_online == any(task_is_online(task) for task in app.tasks))
        ]
    }

    ret["total"] = len(ret['data'])

    return ret


@installed_app_router.post("", response_model=None, summary="安装应用")
async def install_application(app_in: InstalledAppCreate, db_session: DbSession, current_user: CurrentUser):
    """异步安装app"""
    async def run_task():
        svn = Svn(url=app.url, pk=current_user.id)
        if await svn.check_out():
            await svn.install_requirements()
            # session已经关闭，需要重新创建
            session_local = SessionLocal()
            try:
                create(db_session=session_local, app_in=app, user=current_user)
            except Exception as e:
                logger.warning(f"安装应用失败，原因：{e}")
        else:
            logger.warning(f"安装应用失败，原因：svn checkout失败")

    app = app_service.get_by_id(db_session=db_session, pk=app_in.app_id)
    if not app:
        raise HTTPException(404, detail=[{"msg": "安装应用失败，该应用不存在!"}])

    if app.url.endswith(".git"):
        raise HTTPException(500, detail=[{"msg": "安装应用失败，暂时不支持安装git应用!"}])
    else:
        asyncio.create_task(run_task())


@installed_app_router.put("/{app_id}", response_model=InstalledAppRead, summary="更新我的应用信息")
def update_application(app_id: PrimaryKey, app_in: InstalledAppUpdate, db_session: DbSession):
    app = get_by_id(db_session=db_session, pk=app_id)
    if not app:
        raise HTTPException(404, detail=[{"msg": "更新应用失败，该应用不存在！"}])

    app = update(db_session=db_session, app=app, app_in=app_in)
    return app


@installed_app_router.delete("/{app_id}", response_model=None, summary="卸载我的应用")
def delete_application(app_id: PrimaryKey, db_session: DbSession, current_user: CurrentUser):
    installed_app = get_by_id(db_session=db_session, pk=app_id)
    svn = Svn(url=installed_app.application.url, pk=current_user.id)
    try:
        svn.delete_local_repo()
        delete(db_session=db_session, pk=app_id)
    except Exception as e:
        logger.debug(f"卸载应用失败，原因: {e}")
        raise HTTPException(500, detail=[{"msg": f"应用卸载失败！"}])
    remove_dir(pk=app_id, root_dir=STORAGE_MY_APP_DIR)


@installed_app_router.post("/{app_id}/banner", response_model=None, summary="上传我的应用logo")
def upload_file(app_id: PrimaryKey,
                file: Annotated[bytes, File(alias="blob")],
                db_session: DbSession):
    """上传文件，前端数据通过blob字段传递，而不是file
    采用本地存储方案
    todo: 限制上传的文件大小
    """
    installed_app = get_by_id(db_session=db_session, pk=app_id)
    if not installed_app:
        raise HTTPException(404, detail=[{"msg": "上传应用logo失败，该应用不存在！"}])

    if installed_app.banner != installed_app.application.banner:
        remove_old_file(installed_app.banner)

    new_file_path = create_new_file(file=file, pk=installed_app.id, root_dir=STORAGE_MY_APP_DIR)
    update(db_session=db_session, app=installed_app, app_in={"banner": new_file_path})


@installed_app_router.get("/tree", response_model=InstalledAppTree, summary="获取我的应用树结构")
def get_app_tree(current_user: CurrentUser):
    category = {}
    for app in current_user.installed_applications:
        category_name = app.application.category.name
        if not category.__contains__(category_name):
            category[category_name] = {
                **app.application.category.dict(),
                "children": [{**app.dict()}]
            }
        else:
            category[category_name]["children"].append({**app.dict()})

    return {"data": [category[c] for c in category]}


@installed_app_router.get("/{app_id}/readme", response_model=InstalledAppReadme, summary="获取应用的readme")
async def get_app_readme(app_id: PrimaryKey, db_session: DbSession):
    app = get_by_id(db_session=db_session, pk=app_id)
    if not app:
        raise HTTPException(404, detail=[{"msg": "获取应用的readme失败，该应用不存在！"}])
    readme = await Svn(url=app.application.url, pk=app.user_id).cat(file_path="readme.md")
    return {"data": readme}
