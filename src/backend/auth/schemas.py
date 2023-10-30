from typing import Optional, Annotated, Union
from datetime import datetime

from pydantic.networks import EmailStr
from pydantic.functional_validators import BeforeValidator
import bcrypt

from ..core.schemas import MyBaseModel, PrimaryKey, Pagination, NameStr
from ..permission.models import Role


def hash_password(password: str):
    pw = bytes(password, "utf-8")
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(pw, salt)


class UserLoginBase(MyBaseModel):
    username: NameStr


class UserLogin(UserLoginBase):
    password: str


class UserLoginResponse(UserLoginBase):
    avatar: Optional[str] = None
    roles: list[str]
    accessToken: str
    refreshToken: str
    expires: str


class UserBase(MyBaseModel):
    username: NameStr
    avatar: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[EmailStr] = None
    status: bool = True
    remark: Optional[str] = None


class UserCreate(UserBase):
    password: Annotated[str, BeforeValidator(hash_password)]  # 会自动对密码hash
    roles: Optional[list[Union[PrimaryKey, Role]]] = None


class UserUpdate(MyBaseModel):
    username: NameStr
    phone: Optional[str] = None
    email: Optional[EmailStr] = None
    remark: Optional[str] = None


class UserPasswdReset(MyBaseModel):
    password: Annotated[str, BeforeValidator(hash_password)]  # 会自动对密码hash


class UserStatusUpdate(MyBaseModel):
    status: bool


class UserBatchDelete(MyBaseModel):
    ids: list[PrimaryKey]


# 获取某用户的角色列表
class UserRolesRead(MyBaseModel):
    data: list[PrimaryKey]


# 更新用户的角色
class UserRolesUpdate(MyBaseModel):
    roles: list[PrimaryKey]


class UserRead(UserBase):
    id: PrimaryKey
    created_at: datetime


class UserPagination(Pagination):
    data: list[UserRead]
