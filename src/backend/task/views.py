import asyncio
import datetime
import json
from typing import Union, Optional
from uuid import uuid4

from fastapi import APIRouter, HTTPException, WebSocket
from loguru import logger
from croniter import croniter

from .models import Task
from .schemas import TaskPagination, TaskCreate, TaskUpdate, TaskCronUpdate, TaskStatusUpdate, \
    TaskConfigUpdate, TaskConfigRead, TaskTree
from .service import get_by_id, update, delete, create
from .scheduler import update_scheduler, delete_scheduler

from ..application_form import service as app_form_service
from ..core.service import CommonParameters, sort_paginate, DbSession, CurrentUser
from ..core.schemas import PrimaryKey
from ..core.database import SessionLocal
from ..utils.repository import Repository
from ..task_log import log_parser, service as log_service


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
        ret_status, log = await repo.run_app()
        # 解析日志
        log_in = log_parser.parse(ret_status, log, "手动")
        log_service.create(db_session=SessionLocal(),
                           log_in=log_in,
                           task=task)
        return log_in["status"], \
            "任务执行成功，但存在error打印" if log_in["log_type"] == log_parser.SeverityEnum.ERROR else "任务执行成功" \
            if log_in["status"] else "运行任务失败，应用执行报错"

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
    try:
        while True:
            msg = await socket.receive_json()
            logger.debug(f"收到消息：{msg}")
            task = get_by_id(db_session=SessionLocal(), pk=msg["task_id"])
            # 方案一: 单用户任务阻塞
            # await run_task_and_send(task=task, socket=socket)
            # 方案二：任务异步
            asyncio.create_task(run_task_and_send(task=task, socket=socket))
    except Exception as e:
        logger.info(f"webSocket连接断开，原因：{e}")


def create_default_form(config: dict) -> list[dict]:
    return [
        {
            "ControlType": "Text",
            "nameCn": "文本框",
            "id": str(uuid4()),
            "layout": False,
            "data": {
                "fieldName": key,
                "label": key,
                "tip": "",
                "placeholder": "",
                "showRule": "{}",
                "required": False,
                "rule": "[]",
                "default": value,
                "csslist": []
            }
        } for (key, value) in config.items()
    ]


@task_router.get("/{task_id}/config", response_model=TaskConfigRead, summary="获取任务的配置")
def get_task_config(task_id: PrimaryKey, db_session: DbSession, current_user: CurrentUser):
    """优先前端-配置设计-的表单，没有则用项目中默认配置生成的表单(全Text格式)"""
    task = get_by_id(db_session=db_session, pk=task_id)
    # 应用的配置表单
    app_form = app_form_service.get_by_app_id(db_session=db_session, pk=task.application.application.id)
    # 本地配置
    repo = Repository(url=task.application.application.url, pk=current_user.id)
    config = repo.read_task_config(task_id=task_id)

    # 如果应用配置表单不存在或异常，则使用默认的配置表单
    # 如果应用配置表单存在，如果当前任务没有配置，则优先使用应用配置表单中的默认值，而不是项目中的默认配置
    if app_form:
        try:
            form_fields = json.loads(app_form.form)
        except Exception as e:
            logger.warning(f"获取应用的配置表单失败，原因: {e}")
            if not config:
                config = repo.read_default_config()
            form_fields = create_default_form(config)
            return {"data": json.dumps(form_fields)}

        # 将应用表单中的默认值替换成当前任务的实际配置值
        for field in form_fields:
            field_name = field["data"]["fieldName"]
            if field_name not in config:
                continue
            # 有选项的field
            if field["data"].__contains__("itemConfig"):
                field["data"]["itemConfig"]["value"] = config[field_name]
            else:
                field["data"]["default"] = config[field_name]
    else:  # 如果应用配置表单不存在, 则使用默认的配置表单
        if not config:
            config = repo.read_default_config()
        form_fields = create_default_form(config)

    return {"data": json.dumps(form_fields)}


@task_router.put("/{task_id}/config", response_model=None, summary="更新任务的配置")
def update_task_config(task_id: PrimaryKey,
                       task_in: TaskConfigUpdate,
                       db_session: DbSession,
                       current_user: CurrentUser):
    task = get_by_id(db_session=db_session, pk=task_id)
    repo = Repository(url=task.application.application.url, pk=current_user.id)
    config = json.loads(task_in.data)
    repo.write_task_config(task_id=task_id, config=config)


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
