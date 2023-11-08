from typing import Optional, Union, Annotated

from fastapi import APIRouter, HTTPException, File
from loguru import logger
from sqlalchemy.exc import IntegrityError

from .service import get_by_name, get_by_id, create, update, delete
from .schemas import ApplicationPagination, ApplicationRead, ApplicationCreate, ApplicationUpdate, AppStatusUpdate

from ..core.service import CommonParameters, sort_paginate, DbSession
from ..core.schemas import PrimaryKey
from ..utils.storage import remove_old_file, create_new_file

application_router = APIRouter()


@application_router.get("", response_model=ApplicationPagination, summary="获取所有的应用列表")
def get_applications(
        common: CommonParameters,
        category_id: Optional[int] = None,
        status: Optional[bool] = None
):
    filter_spec = []
    if category_id:
        filter_spec.append({"field": "category_id", 'op': '==', 'value': category_id})
    if status is not None:
        filter_spec.append({"field": "status", 'op': '==', 'value': status})

    pagination = sort_paginate(model="Application", filter_spec=filter_spec, **common)
    # 获取当前用户的已安装app，并修改is_installed的状态
    # todo
    res = []
    for app in pagination["data"]:
        app_data = app.dict()
        app_data['is_installed'] = True
        res.append(app_data)

    return {
        **pagination,
        "data": res
    }


@application_router.post("", response_model=ApplicationRead, summary="上架应用")
def create_application(app_in: ApplicationCreate, db_session: DbSession):
    app = get_by_name(db_session=db_session, name=app_in.name)
    if app:
        raise HTTPException(422, detail=[{"msg": "上架应用失败，该应用的名称已经存在!"}])

    try:
        app = create(db_session=db_session, app_in=app_in)
    except IntegrityError:
        logger.warning(f"创建应用失败，原因：{IntegrityError}")
        raise HTTPException(500, detail=[{"msg": "上架应用失败！"}])
    return app


@application_router.put("/{app_id}", response_model=ApplicationRead, summary="更新应用信息, 更新应用状态")
def update_application(app_id: PrimaryKey,
                       app_in: Union[ApplicationUpdate, AppStatusUpdate],
                       db_session: DbSession):
    app = get_by_id(db_session=db_session, pk=app_id)
    if not app:
        raise HTTPException(404, detail=[{"msg": "更新应用失败，该应用不存在！"}])
    try:
        app = update(db_session=db_session, app=app, app_in=app_in)
    except IntegrityError:
        logger.warning(f"更新应用失败，原因：{IntegrityError}")
        raise HTTPException(500, detail=[{"msg": "更新应用失败！"}])
    return app


@application_router.delete("/{app_id}", response_model=None, summary="删除应用")
def delete_application(app_id: PrimaryKey, db_session: DbSession):
    app = get_by_id(db_session=db_session, pk=app_id)
    if app:
        remove_old_file(app.banner)  # 清理该应用的图片
    else:
        return

    try:
        delete(db_session=db_session, pk=app_id)
    except IntegrityError:
        logger.debug(f"删除应用失败，原因: {IntegrityError}")
        raise HTTPException(500, detail=[{"msg": f"应用删除失败！存在用户已经安装了该应用"}])


@application_router.post("/{app_id}/banner", response_model=None, summary="上传应用logo")
def upload_file(app_id: PrimaryKey,
                file: Annotated[bytes, File(alias="blob")],
                db_session: DbSession):
    """上传文件，前端数据通过blob字段传递，而不是file
    采用本地存储方案
    todo: 限制上传的文件大小
    """
    app = get_by_id(db_session=db_session, pk=app_id)
    if not app:
        raise HTTPException(404, detail=[{"msg": "上传应用logo失败，该应用不存在！"}])

    remove_old_file(app.banner)
    new_file_path = create_new_file(file=file, pk=app.id, root_dir="apps")

    update(db_session=db_session, app=app, app_in={"banner": new_file_path})
