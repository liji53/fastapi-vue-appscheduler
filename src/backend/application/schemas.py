from typing import Optional

from pydantic.networks import HttpUrl

from ..core.schemas import Pagination, MyBaseModel, NameStr


class ApplicationRead(MyBaseModel):
    name: NameStr
    is_installed: bool = False
    type_id: Optional[int] = None
    banner: Optional[HttpUrl] = None
    description: Optional[str] = None


class ApplicationPagination(Pagination):
    data: list[ApplicationRead]
