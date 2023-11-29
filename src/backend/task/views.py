import asyncio
import datetime
import json
from typing import Union, Optional

from fastapi import APIRouter, HTTPException, WebSocket
from loguru import logger

from .models import Task
from .schemas import TaskPagination, TaskCreate, TaskUpdate, TaskCronUpdate, TaskStatusUpdate
from .service import get_by_id, update, delete, create
from .scheduler import update_scheduler, delete_scheduler

from ..core.service import CommonParameters, sort_paginate, DbSession, CurrentUser
from ..core.schemas import PrimaryKey
from ..core.database import SessionLocal
from ..utils.repository import Repository


task_router = APIRouter()


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
                task_in: Union[TaskCronUpdate, TaskStatusUpdate, TaskUpdate],
                db_session: DbSession):

    task = get_by_id(db_session=db_session, pk=task_id)
    if not task:
        raise HTTPException(404, detail=[{"msg": "更新任务失败，该任务不存在！"}])

    # 更新/设置 定位任务
    if isinstance(task_in, TaskCronUpdate):
        update_scheduler(old_task=task, status=task.status, cron=task_in.cron)

    # 更新状态，启动/暂停 定时任务
    if isinstance(task_in, TaskStatusUpdate):
        update_scheduler(old_task=task, status=task_in.status, cron=task.cron)

    update(db_session=db_session, task=task, task_in=task_in)


@task_router.delete("/{task_id}", response_model=None, summary="删除任务")
def delete_task(task_id: PrimaryKey, db_session: DbSession):
    try:
        delete(db_session=db_session, pk=task_id)
    except Exception as e:
        logger.debug(f"删除任务失败，原因: {e}")
        raise HTTPException(500, detail=[{"msg": f"删除任务失败！"}])

    # 数据库删除成功，才能删除定时任务
    delete_scheduler(task_id=task_id)


async def run_task_and_send(task: Task, socket: WebSocket):
    async def execute_task():
        if not task:
            return False, "运行任务失败，该任务不存在！"
        repo = Repository(url=task.application.application.url, pk=task.application.user_id)
        return await repo.run_app()

    # 单用户阻塞实现：如果一个用户同时执行了多个任务，后面的任务会阻塞
    is_success, result = await execute_task()
    tmp = {
        "name": "任务结果",
        "list": [{
            "avatar": "https://gw.alipayobjects.com/zos/rmsportal/ThXAXghbEsBCCSDihZxY.png",
            "title": f"{task.name}",
            "datetime": datetime.datetime.today().strftime("%m-%d %H:%M:%S"),
            "description": f"{result}",
            "extra": '成功' if is_success else '失败',
            "status": "success" if is_success else "danger",
         }]
    }
    await socket.send_text(json.dumps(tmp))


@task_router.websocket("/ws")
async def run_task(socket: WebSocket):
    """用户手动执行任务，服务器通知任务的执行结果"""
    await socket.accept()

    while True:
        msg = await socket.receive_json()
        logger.debug(f"收到消息：{msg}")
        task = get_by_id(db_session=SessionLocal(), pk=msg["task_id"])
        # 方案一: 单用户任务阻塞
        # await run_task_and_send(task=task, socket=socket)
        # 方案二：任务异步
        asyncio.create_task(run_task_and_send(task=task, socket=socket))
