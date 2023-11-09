from typing import Optional

from .models import ApplicationInstalled
from .schemas import InstalledAppUpdate

from ..auth.models import User
from ..application.models import Application


def get_by_id(*, db_session, pk: int) -> Optional[ApplicationInstalled]:
    return db_session.query(ApplicationInstalled).filter(ApplicationInstalled.id == pk).one_or_none()


def create(*, db_session, app_in: Application, user: User) -> ApplicationInstalled:
    """安装app"""
    app = ApplicationInstalled(
        **app_in.dict(exclude=["id", "url", "status", "category_id", "created_at", "updated_at"])
    )
    app.is_online = False
    # todo: 获取版本
    app.application = app_in
    app.user = user

    db_session.add(app)
    db_session.commit()
    return app


def update(*, db_session, app: ApplicationInstalled, app_in: [InstalledAppUpdate, dict]) -> ApplicationInstalled:
    app_data = app.dict()
    if isinstance(app_in, dict):
        update_data = app_in
    else:
        update_data = app_in.model_dump()

    for field in app_data:
        if field in update_data:
            setattr(app, field, update_data[field])

    db_session.commit()
    return app


def delete(*, db_session, pk: int):
    db_session.query(ApplicationInstalled).filter(ApplicationInstalled.id == pk).delete()
    db_session.commit()
