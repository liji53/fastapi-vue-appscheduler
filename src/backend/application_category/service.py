from typing import Optional

from .models import ApplicationCategory
from .schemas import ApplicationCategoryCreate


def create(*, db_session, app_category_in: ApplicationCategoryCreate) -> ApplicationCategory:
    """创建app"""
    app = ApplicationCategory(**app_category_in.model_dump())

    db_session.add(app)
    db_session.commit()
    return app


def get_all(*, db_session) -> list[ApplicationCategory]:
    return db_session.query(ApplicationCategory).all()


def get_by_name(*, db_session, category_name: str) -> Optional[ApplicationCategory]:
    return db_session.query(ApplicationCategory).filter(ApplicationCategory.name == category_name).one_or_none()
