from typing import Optional

from .models import ApplicationForm
from .schemas import ApplicationFormUpdate


def get_by_app_id(*, db_session, pk: int) -> Optional[ApplicationForm]:
    """pk 用的是app_id, 而不是ApplicationForm的主键"""
    return db_session.query(ApplicationForm).filter(ApplicationForm.application_id == pk).one_or_none()


def create(*, db_session, form_in: ApplicationFormUpdate, pk: int) -> ApplicationForm:
    """pk 指的时app_id"""
    app_form = ApplicationForm(**form_in.model_dump())
    app_form.application_id = pk
    db_session.add(app_form)
    db_session.commit()
    return app_form


def update(*, db_session, app_form: ApplicationForm, form_in: ApplicationFormUpdate) -> ApplicationForm:
    app_form.form = form_in.form
    db_session.commit()
    return app_form
