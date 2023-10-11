from typing import Optional, Annotated, Union

from pydantic import Field
from pydantic.networks import EmailStr
from pydantic.functional_validators import BeforeValidator
import bcrypt

from ..core.schemas import MyBaseModel, PrimaryKey
from ..permission.models import Role


def hash_password(password: str):
    pw = bytes(password, "utf-8")
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(pw, salt)


class UserBase(MyBaseModel):
    username: str
    email: Optional[EmailStr] = None


class UserLogin(UserBase):
    password: str


class UserRegister(UserBase):
    """需要对密码进行哈希"""
    password: Annotated[str, BeforeValidator(hash_password)]
    roles: list[Union[int, Role]]


class UserLoginResponse(MyBaseModel):
    username: str
    roles: list[str]
    accessToken: str
    refreshToken: str
    expires: str


class UserRead(UserBase):
    id: PrimaryKey
    role: Optional[str] = Field(None, nullable=True)
