import asyncio
from typing import Union, Optional

from fastapi import APIRouter, HTTPException, WebSocket
from loguru import logger

from .schemas import TaskPagination, TaskCreate, TaskUpdate, TaskCronUpdate, TaskStatusUpdate
from .service import get_by_id, update, delete, create

from ..core.service import CommonParameters, sort_paginate, DbSession, CurrentUser
from ..core.schemas import PrimaryKey
from ..core.database import SessionLocal
from ..utils.repository import Repository


task_router = APIRouter()
running_tasks: dict[PrimaryKey, asyncio.Task] = {}  # 用于存储正在执行中的任务


@task_router.get("", response_model=TaskPagination, summary="获取任务列表")
def get_tasks(common: CommonParameters,
              current_user: CurrentUser,
              project_id: Optional[PrimaryKey] = None,
              status: Optional[bool] = None):
    filter_spec = []
    if project_id is not None:
        filter_spec.append({"field": "project_id", 'op': '==', 'value': project_id})
    else:
        project_ids = [project.id for project in current_user.projects]
        filter_spec.append({"field": "project_id", 'op': 'in', 'value': project_ids})
    if status is not None:
        filter_spec.append({"field": "status", 'op': '==', 'value': status})

    pagination = sort_paginate(model="Task", filter_spec=filter_spec, **common)
    ret = []
    for task in pagination["data"]:
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


@task_router.post("/{task_id}/run", response_model=None, summary="运行任务")
async def run_task(task_id: PrimaryKey, db_session: DbSession, current_user: CurrentUser):
    task = get_by_id(db_session=db_session, pk=task_id)
    if not task:
        raise HTTPException(404, detail=[{"msg": "运行任务失败，该任务不存在！"}])
    repo = Repository(url=task.application.application.url, pk=current_user.id)
    async_task = await repo.run_app()
    running_tasks[task_id] = async_task
    if async_task is None:
        logger.warning("运行任务失败，该应用不存在main.py")
        raise HTTPException(500, detail=[{"msg": f"运行任务失败，该应用不存在main.py"}])


@task_router.websocket("/{task_id}/ws")
async def run_task_result(socket: WebSocket, task_id: PrimaryKey):
    """服务器主动通知客户端任务的执行结果"""
    await socket.accept()
    db_task = get_by_id(pk=task_id, db_session=SessionLocal())
    task = running_tasks.get(task_id)
    while True:
        if task and await task.done():
            result = task.result()
            await socket.send_text(f"{db_task.name}的执行结果：{result}")
            await socket.close()
            break
