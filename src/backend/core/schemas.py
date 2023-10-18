from pydantic import BaseModel
from pydantic.types import conint, constr
from datetime import datetime

PrimaryKey = conint(gt=0)
NameStr = constr(strip_whitespace=True, min_length=1)  # 不能是空白行


class MyBaseModel(BaseModel):
    class Config:
        from_attributes = True  # orm_mode = True
        validate_assignment = True
        arbitrary_types_allowed = True
        str_strip_whitespace = True

        # datetime 的格式
        json_encoders = {
            datetime: lambda v: v.strftime("%Y-%m-%dT%H:%M:%SZ") if v else None,
        }


class Pagination(MyBaseModel):
    itemsPerPage: int
    page: int
    total: int
