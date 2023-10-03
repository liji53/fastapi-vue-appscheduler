from typing import Optional, List, Annotated

from pydantic import Field, field_validator
from pydantic.networks import EmailStr
from pydantic.functional_validators import BeforeValidator
import bcrypt

from ..core.schemas import AppBaseModel, PrimaryKey


def hash_password(password: str):
    pw = bytes(password, "utf-8")
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(pw, salt)


class UserBase(AppBaseModel):
    username: str
    email: Optional[EmailStr] = None


class UserLogin(UserBase):
    password: str


class UserRegister(UserBase):
    """需要对密码进行哈希"""
    password: Annotated[str, BeforeValidator(hash_password)]


class UserLoginResponse(AppBaseModel):
    accessToken: str


class UserRead(UserBase):
    id: PrimaryKey
    role: Optional[str] = Field(None, nullable=True)
