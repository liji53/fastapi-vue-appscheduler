from .models import Application
from .schemas import ApplicationCreate
from ..application_category import service as app_category_service


def create(*, db_session, application_in: ApplicationCreate) -> Application:
    """创建app"""
    category = None
    if application_in.category:
        category = app_category_service.get_by_name(db_session=db_session, category_name=application_in.category.name)

    app = Application(**application_in.model_dump(exclude=["category"]))
    if category:
        app.category = category

    db_session.add(app)
    db_session.commit()
    return app


def get_all(*, db_session) -> list[Application]:
    return db_session.query(Application).all()
