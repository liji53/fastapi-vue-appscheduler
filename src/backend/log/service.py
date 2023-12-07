from typing import Optional
from sqlalchemy.orm import Session
from sqlalchemy.sql import func

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


def get_failed_count(*, db_session: Session, task_ids: list[int]):
    # 获取最近一条log的子查询
    subquery = db_session.query(Log.task_id, func.max(Log.created_at).label('max_created_at')) \
        .filter(Log.task_id.in_(task_ids)).group_by(Log.task_id).subquery()
    # 统计最近一条日志执行失败的数量
    return db_session.query(Log) \
        .join(subquery,
              (Log.task_id == subquery.c.task_id) &
              (Log.created_at == subquery.c.max_created_at) &
              (Log.status == False)
              ).count()

