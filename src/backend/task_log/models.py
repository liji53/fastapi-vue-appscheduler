from enum import Enum
from sqlalchemy import Column, Integer, String, ForeignKey, Text, Boolean, Enum as EnumSQL
from ..core.database import Base, DateTimeMixin


class SeverityEnum(Enum):
    FATAL = 'fatal'
    ERROR = 'error'
    WARNING = 'warning'
    OTHER = 'other'


class Log(Base, DateTimeMixin):
    id = Column(Integer, primary_key=True)
    status = Column(Boolean, nullable=False, comment="任务执行的结果状态")
    log_type = Column(EnumSQL(SeverityEnum), nullable=False, comment="任务执行后生成的日志的级别")
    execute_type = Column(String(16), nullable=False, comment="任务执行的方式")
    content = Column(Text, comment="任务执行时生成的日志内容")

    task_id = Column(Integer, ForeignKey("task.id", ondelete='cascade'))
