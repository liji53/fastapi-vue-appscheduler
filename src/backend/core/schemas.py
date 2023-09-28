from pydantic import BaseModel
from pydantic.types import conint
from datetime import datetime

PrimaryKey = conint(gt=0)


class AppBaseModel(BaseModel):
    class Config:
        from_attributes = True  # orm_mode = True
        validate_assignment = True
        arbitrary_types_allowed = True
        str_strip_whitespace = True

        # datetime 的格式
        json_encoders = {
            datetime: lambda v: v.strftime("%Y-%m-%dT%H:%M:%SZ") if v else None,
        }
