import datetime
from typing import Union, Optional

from fastapi import APIRouter, HTTPException
from loguru import logger
from croniter import croniter

from .schemas import TaskPagination, TaskCreate, TaskUpdate, TaskCronUpdate, TaskStatusUpdate, TaskTree
from .service import get_by_id, update, delete, create
from .scheduler import update_scheduler

from ..core.service import CommonParameters, sort_paginate, DbSession, CurrentUser
from ..core.schemas import PrimaryKey


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
            "next_at": croniter(task.cron).get_next(datetime.datetime).strftime("%Y-%m-%d %M:%H:%S")
            if task.cron and task.status else None,
            "project": task.project.name,
            "url": task.application.application.url
        })

    return {**pagination, "data": ret}


@task_router.post("", response_model=None, summary="新建任务")
def create_task(task_in: TaskCreate, db_session: DbSession):
    try:
        create(db_session=db_session, task_in=task_in)
    except Exception as e:
        logger.warning(f"创建任务失败，原因：{e}")
        raise HTTPException(500, detail=[{"msg": "创建任务失败！"}])


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


@task_router.get("/tree", response_model=TaskTree, summary="获取项目-任务的树结构")
def get_task_tree(current_user: CurrentUser):
    project_tasks = {}
    for project in current_user.projects:
        for task in project.tasks:
            if not project_tasks.__contains__(project.id):
                project_tasks[project.id] = {
                    "name": project.name,
                    "children": [{
                        "id": task.id,
                        "name": task.name,
                    }]
                }
            else:
                project_tasks[project.id]["children"].append({
                    "id": task.id,
                    "name": task.name,
                })

    return {"data": [project_tasks[p] for p in project_tasks]}
