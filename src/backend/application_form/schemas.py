from typing import Optional

from ..core.schemas import MyBaseModel, PrimaryKey


class ApplicationFormRead(MyBaseModel):
    form: Optional[str] = None


class ApplicationFormUpdate(MyBaseModel):
    form: str
