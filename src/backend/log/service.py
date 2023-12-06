from typing import Optional

from .models import Log

from ..task.models import Task


def get_by_id(*, db_session, pk: int) -> Optional[Log]:
    return db_session.query(Log).filter(Log.id == pk).one_or_none()


def create(*, db_session, log_in: dict, task: Task):
    log = Log(**log_in)
    log.task_id = task.id
    db_session.add(log)
    db_session.commit()


def delete(*, db_session, pk: int):
    db_session.query(Log).filter(Log.id == pk).delete()
    db_session.commit()
