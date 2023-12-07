from fastapi import APIRouter, HTTPException
from loguru import logger

from .schemas import ApplicationCategoryPagination, ApplicationCategoryUpdate, ApplicationCategoryCreate
from .service import create, update, get_by_id, delete

from ..core.service import CommonParameters, sort_paginate
from ..core.database import DbSession
from ..core.schemas import PrimaryKey


app_category_router = APIRouter()


@app_category_router.get("", response_model=ApplicationCategoryPagination, summary="获取应用类别列表")
def get_app_categories(common: CommonParameters):
    pagination = sort_paginate(model="ApplicationCategory", **common)
    ret = []
    for category in pagination["data"]:
        ret.append({
            **category.dict(),
            "app_count": len(category.applications),
            "installed_app_count": len([app for app in category.applications if app.installed_applications]),
            "installed_sum_count": sum([len(app.installed_applications) for app in category.applications])
        })

    return {**pagination, "data": ret}


@app_category_router.post("", response_model=None, summary="创建应用分类")
def create_app_category(app_category_in: ApplicationCategoryCreate, db_session: DbSession):
    try:
        create(db_session=db_session, app_category_in=app_category_in)
    except Exception as e:
        logger.warning(f"创建应用分类失败，原因：{e}")
        raise HTTPException(500, detail=[{"msg": "创建应用分类失败！"}])


@app_category_router.put("/{app_category_id}", response_model=None, summary="更新应用分类的信息")
def update_app_category(app_category_id: PrimaryKey, category_in: ApplicationCategoryUpdate, db_session: DbSession):
    app_category = get_by_id(db_session=db_session, pk=app_category_id)
    if not app_category:
        raise HTTPException(404, detail=[{"msg": "更新应用分类失败，该分类不存在！"}])

    update(db_session=db_session, app_category=app_category, app_category_in=category_in)


@app_category_router.delete("/{app_category_id}", response_model=None, summary="删除应用分类")
def delete_app_category(app_category_id: PrimaryKey, db_session: DbSession):
    try:
        delete(db_session=db_session, pk=app_category_id)
    except Exception as e:
        logger.debug(f"删除应用分类失败，原因: {e}")
        raise HTTPException(500, detail=[{"msg": f"删除应用分类失败, 请先删除该分类下的应用"}])
