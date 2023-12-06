from typing import Optional, Union

from .models import Task
from .schemas import TaskCreate, TaskUpdate, TaskCronUpdate, TaskStatusUpdate
from sqlalchemy.orm import Session


def get_by_id(*, db_session, pk: int) -> Optional[Task]:
    return db_session.query(Task).filter(Task.id == pk).one_or_none()


def get_by_ids(*, db_session, pks: list[int]) -> list[Task]:
    return db_session.query(Task).filter(Task.id.in_(pks)).all()


def get_schedule_tasks(*, db_session: Session) -> list[Task]:
    return db_session.query(Task).filter(Task.status).filter(Task.cron.isnot(None)).all()


def create(*, db_session, task_in: TaskCreate) -> Task:
    task = Task(**task_in.model_dump())
    db_session.add(task)
    db_session.commit()
    return task


def update(*, db_session, task: Task, task_in: Union[TaskUpdate, TaskCronUpdate, TaskStatusUpdate]) -> Task:
    db_data = task.dict()
    update_data = task_in.model_dump()

    for field in db_data:
        if field in update_data:
            setattr(task, field, update_data[field])

    db_session.commit()
    return task


def delete(*, db_session: Session, pk: int):
    db_session.query(Task).filter(Task.id == pk).delete()
    db_session.commit()
