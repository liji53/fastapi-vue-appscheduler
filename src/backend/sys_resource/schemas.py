from ..core.schemas import MyBaseModel


class SysResource(MyBaseModel):
    cpu: float
    memory: float
    disk: int
    full_disk: int

