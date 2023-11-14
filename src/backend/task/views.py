from typing import Union

from fastapi import APIRouter, HTTPException
from loguru import logger

from .schemas import TaskPagination, TaskCreate, TaskUpdate, TaskCronUpdate, TaskStatusUpdate
from .service import get_by_id, update, delete, create

from ..core.service import CommonParameters, sort_paginate, DbSession
from ..core.schemas import PrimaryKey


task_router = APIRouter()


@task_router.get("", response_model=TaskPagination, summary="获取任务列表")
def get_tasks(common: CommonParameters):
    pagination = sort_paginate(model="Task", **common)
    ret = []
    for task in pagination["data"]:
        logger.debug(**task.dict())
        ret.append({
            **task.dict(),
            "project": task.project.name
        })

    return {**pagination, "data": ret}


@task_router.post("", response_model=None, summary="新建任务")
def create_task(task_in: TaskCreate, db_session: DbSession):
    try:
        create(db_session=db_session, task_in=task_in)
    except Exception as e:
        logger.warning(f"创建项目失败，原因：{e}")
        raise HTTPException(500, detail=[{"msg": "创建项目失败！"}])


@task_router.put("/{task_id}", response_model=None, summary="更新任务信息、使能任务状态、设置定时")
def update_task(task_id: PrimaryKey,
                task_in: Union[TaskUpdate, TaskStatusUpdate, TaskCronUpdate],
                db_session: DbSession):
    task = get_by_id(db_session=db_session, pk=task_id)
    if not task:
        raise HTTPException(404, detail=[{"msg": "更新任务失败，该任务不存在！"}])

    update(db_session=db_session, task=task, task_in=task_in)


@task_router.delete("/{task_id}", response_model=None, summary="删除任务")
def delete_task(task_id: PrimaryKey, db_session: DbSession):
    try:
        delete(db_session=db_session, pk=task_id)
    except Exception as e:
        logger.debug(f"删除任务失败，原因: {e}")
        raise HTTPException(500, detail=[{"msg": f"删除任务失败！"}])
