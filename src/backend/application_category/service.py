from typing import Optional

from .models import ApplicationCategory
from .schemas import ApplicationCategoryCreate, ApplicationCategoryUpdate


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


def get_by_id(*, db_session, pk: int) -> Optional[ApplicationCategory]:
    return db_session.query(ApplicationCategory).filter(ApplicationCategory.id == pk).one_or_none()


def update(*, db_session, app_category: ApplicationCategory, app_category_in: ApplicationCategoryUpdate):
    db_data = app_category.dict()
    update_data = app_category_in.model_dump()

    for field in db_data:
        if field in update_data:
            setattr(app_category, field, update_data[field])

    db_session.commit()


def delete(*, db_session, pk: int):
    db_session.query(ApplicationCategory).filter(ApplicationCategory.id == pk).delete()
    db_session.commit()
