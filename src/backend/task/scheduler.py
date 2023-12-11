import asyncio

from loguru import logger
from apscheduler.triggers.cron import CronTrigger

from .service import get_by_id

from ..core.scheduler import scheduler
from ..utils.repository import Repository
from ..core.database import SessionLocal
from ..task_log import log_parser, service as log_service

# 只暴露 update和delete
__all__ = ["update_scheduler", "delete_scheduler"]


def run_job(task_id: int):
    """scheduler 添加的运行任务"""
    task = get_by_id(db_session=SessionLocal(), pk=task_id)
    repo = Repository(url=task.application.application.url, pk=task.application.user_id)
    ret_status, log = asyncio.run(repo.run_app())
    log_service.create(db_session=SessionLocal(),
                       log_in=log_parser.parse(ret_status, log, "定时"),
                       task=task)


def update_scheduler(old_task, status, cron):
    job = scheduler.get_job(job_id=str(old_task.id))

    if job and (not cron or not status):
        logger.debug(f"删除定时任务<{old_task.name}>")
        job.remove()
    elif job and status and cron:
        logger.debug(f"更新定时任务<{old_task.name} - {cron}>")
        scheduler.reschedule_job(job_id=str(old_task.id), trigger=CronTrigger.from_crontab(expr=cron))
    elif not job and status and cron:
        logger.debug(f"添加定时任务<{old_task.name} - {cron}>")
        scheduler.add_job(func=run_job,
                          args=[old_task.id],
                          trigger=CronTrigger.from_crontab(expr=cron),
                          id=str(old_task.id))


def delete_scheduler(task_id: int):
    job = scheduler.get_job(job_id=str(task_id))
    if job:
        logger.debug(f"删除定时任务<{task_id}>")
        job.remove()
