from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.executors.pool import ThreadPoolExecutor
from loguru import logger

from ..task.service import get_schedule_tasks
from ..core.database import SessionLocal

#
__all__ = ["scheduler", "init_scheduler"]


scheduler_config = {
    # "jobstores": {
    #     'default': SQLAlchemyJobStore(url='sqlite:///jobs.sqlite')
    # },
    "executors": {
        # ProcessPoolExecutor更适合计算密集型任务
        "default": ThreadPoolExecutor(max_workers=20)
    }
}
scheduler = AsyncIOScheduler(**scheduler_config)


def init_scheduler() -> None:
    """初始化，启动apScheduler"""
    from ..task.scheduler import update_scheduler  # 可以避免循环import
    scheduler.start()

    tasks = get_schedule_tasks(db_session=SessionLocal())
    for task in tasks:
        if scheduler.get_job(job_id=str(task.id)):
            logger.info(f"存在定时任务: {task}")
            continue
        update_scheduler(old_task=task, status=task.status, cron=task.cron)
