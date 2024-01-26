from sqlalchemy import Column, String, Integer, ForeignKey
from ..core.database import Base, DateTimeMixin


class ApplicationForm(Base, DateTimeMixin):
    id = Column(Integer, primary_key=True)
    form = Column(String(8192), nullable=False, comment="由低码组件自动生成的应用配置表单的json数据")

    application_id = Column(Integer, ForeignKey("application.id", ondelete='cascade'))
