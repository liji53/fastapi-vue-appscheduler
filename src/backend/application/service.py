from typing import Optional, Union

from loguru import logger

from .models import Application
from .schemas import ApplicationCreate, ApplicationUpdate, AppStatusUpdate

from ..application_category import service as app_category_service


def get_by_name(*, db_session, name: str) -> Optional[Application]:
    return db_session.query(Application).filter(Application.name == name).one_or_none()


def get_by_id(*, db_session, pk: int) -> Optional[Application]:
    return db_session.query(Application).filter(Application.id == pk).one_or_none()


def create(*, db_session, app_in: ApplicationCreate) -> Application:
    """创建app"""
    category = None
    if app_in.category_id:
        category = app_category_service.get_by_id(db_session=db_session, pk=app_in.category_id)

    app = Application(**app_in.model_dump(exclude=["category_id"]))
    if category:
        app.category = category

    db_session.add(app)
    db_session.commit()
    return app


def update(*, db_session,
           app: Application,
           app_in: Union[ApplicationUpdate, AppStatusUpdate, dict]) -> Application:

    app_data = app.dict()
    if isinstance(app_in, dict):
        update_data = app_in
    else:
        update_data = app_in.model_dump()

    logger.debug(app_data)
    logger.debug(update_data)

    for field in app_data:
        if field in update_data:
            setattr(app, field, update_data[field])

    db_session.commit()
    return app


def delete(*, db_session, pk: int):
    db_session.query(Application).filter(Application.id == pk).delete()
    db_session.commit()
