from fastapi import APIRouter, HTTPException
from loguru import logger

from .schemas import ApplicationFormRead, ApplicationFormUpdate
from .service import get_by_app_id, update, create

from ..core.database import DbSession
from ..core.schemas import PrimaryKey


app_form_router = APIRouter()


@app_form_router.get("/{app_id}", response_model=ApplicationFormRead, summary="获取应用配置表单的lowcode json数据")
def get_app_form(app_id: PrimaryKey, db_session: DbSession):
    form = get_by_app_id(db_session=db_session, pk=app_id)
    if not form:
        return {"form": None}
    return form


@app_form_router.put("/{app_id}", response_model=None, summary="保存(没有则创建，有则更新)应用配置表单的lowcode json数据")
def create_or_update_app_form(app_id: PrimaryKey, db_session: DbSession, form_in: ApplicationFormUpdate):
    app_form = get_by_app_id(db_session=db_session, pk=app_id)
    if not app_form:
        create(db_session=db_session, form_in=form_in, pk=app_id)
        return

    try:
        update(db_session=db_session, app_form=app_form, form_in=form_in)
    except Exception as e:
        logger.warning(f"更新应用表单失败，原因：{e}")
        raise HTTPException(500, detail=[{"msg": "更新应用表单失败！"}])
