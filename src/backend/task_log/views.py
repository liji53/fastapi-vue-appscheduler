from typing import Optional, Annotated

from fastapi import APIRouter, HTTPException, Query
from loguru import logger

from .schemas import LogPagination, LogContentRead, LogRecently, LogCreate
from .service import delete, get_by_id, get_recently_by_task_id, create
from .log_parser import parse

from ..core.service import CommonParameters, sort_paginate, DbSession, CurrentUser
from ..core.schemas import PrimaryKey
from ..task import service as task_service
from ..task.models import Task


log_router = APIRouter()


@log_router.get("", response_model=LogPagination, summary="获取日志列表")
def get_logs(common: CommonParameters,
             current_user: CurrentUser,
             db_session: DbSession,
             task_ids: Annotated[Optional[list[int]], Query()] = None,
             status: Optional[bool] = None,
             log_type: Optional[str] = None):
    filter_spec = []
    if task_ids is None:
        # todo: admin需要查看所有的log
        task_ids = [task.id for project in current_user.projects for task in project.tasks]

    filter_spec.append({"field": "task_id", 'op': 'in', 'value': task_ids})
    if status is not None:
        filter_spec.append({"field": "status", 'op': '==', 'value': status})

    if log_type is not None:
        filter_spec.append({"field": "log_type", 'op': '==', 'value': log_type})

    # 缓存查找到的任务
    tasks = task_service.get_by_ids(db_session=db_session, pks=task_ids)
    cache_task: dict[int, Task] = {task.id: task for task in tasks}

    pagination = sort_paginate(model="Log", filter_spec=filter_spec, **common)
    ret = []
    for log in pagination["data"]:
        ret.append({
            **log.dict(exclude=["content"]),
            "project_name": cache_task[log.task_id].project.name,
            "task_name": cache_task[log.task_id].name
        })

    return {**pagination, "data": ret}


@log_router.delete("/{log_id}", response_model=None, summary="删除日志")
def delete_log(log_id: PrimaryKey, db_session: DbSession):
    try:
        delete(db_session=db_session, pk=log_id)
    except Exception as e:
        logger.debug(f"删除日志失败，原因: {e}")
        raise HTTPException(500, detail=[{"msg": f"删除日志失败"}])


@log_router.get("/{log_id}/content", response_model=LogContentRead, summary="获取日志的详细内容")
def get_log_content(log_id: PrimaryKey, db_session: DbSession):
    log = get_by_id(db_session=db_session, pk=log_id)
    if not log:
        raise HTTPException(404, detail=[{"msg": f"获取日志失败，不存在该日志"}])
    return {"data": log.content}


@log_router.get("/recently", response_model=LogRecently, summary="根据任务，获取最新一条日志的内容")
def get_log_recently(task_id: int, db_session: DbSession):
    log = get_recently_by_task_id(db_session=db_session, task_id=task_id)
    if not log:
        raise HTTPException(404, detail=[{"msg": f"该任务最近没有日志"}])
    return log


@log_router.post("", response_model=None, summary="前端执行应用之后，上传到后台的应用执行日志")
def create_log(db_session: DbSession, log_in: LogCreate):
    task = task_service.get_by_id(db_session=db_session, pk=log_in.task_id)
    if not task:
        raise HTTPException(404, detail=[{"msg": "提交任务的执行日志失败，该任务不存在！"}])
    log_dict = parse(running_status=log_in.status, log=log_in.content, execute_type=log_in.execute_type)
    create(db_session=db_session, log_in=log_dict, task=task)
