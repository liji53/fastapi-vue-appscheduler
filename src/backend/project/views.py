
from fastapi import APIRouter, HTTPException
from loguru import logger

from .schemas import ProjectPagination, ProjectCreate, ProjectUpdate
from .service import get_by_id, update, delete, create

from ..core.service import CommonParameters, sort_paginate, DbSession, CurrentUser
from ..core.schemas import PrimaryKey
from ..log import service as log_service


project_router = APIRouter()


@project_router.get("", response_model=ProjectPagination, summary="获取项目列表")
def get_projects(common: CommonParameters, db_session: DbSession):
    project_pagination = sort_paginate(model="Project", **common)

    ret = []
    for project in project_pagination["data"]:
        ret.append({
            **project.dict(),
            "task_count": len(project.tasks),
            "online_count": len([task for task in project.tasks if task.cron and task.status]),
            "failed_count": log_service.get_failed_count(db_session=db_session,
                                                         task_ids=[task.id for task in project.tasks])
        })

    return {**project_pagination, "data": ret}


@project_router.post("", response_model=None, summary="创建项目")
def create_project(project_in: ProjectCreate, db_session: DbSession, current_user: CurrentUser):
    try:
        create(db_session=db_session, project_in=project_in, user=current_user)
    except Exception as e:
        logger.warning(f"创建项目失败，原因：{e}")
        raise HTTPException(500, detail=[{"msg": "创建项目失败！"}])


@project_router.put("/{project_id}", response_model=None, summary="更新我的应用信息")
def update_application(project_id: PrimaryKey, project_in: ProjectUpdate, db_session: DbSession):
    project = get_by_id(db_session=db_session, pk=project_id)
    if not project:
        raise HTTPException(404, detail=[{"msg": "更新项目失败，该项目不存在！"}])

    update(db_session=db_session, project=project, project_in=project_in)


@project_router.delete("/{project_id}", response_model=None, summary="删除项目")
def delete_project(project_id: PrimaryKey, db_session: DbSession):
    try:
        delete(db_session=db_session, pk=project_id)
    except Exception as e:
        logger.debug(f"删除项目失败，原因: {e}")
        raise HTTPException(500, detail=[{"msg": f"删除项目失败, 请先删除该项目的任务"}])
