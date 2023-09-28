from typing import Optional, List

from pydantic import Field
from pydantic.networks import EmailStr

from ..core.schemas import AppBaseModel, PrimaryKey


class UserBase(AppBaseModel):
    username: str
    email: Optional[EmailStr] = None


class UserLogin(UserBase):
    password: str


class UserLoginResponse(AppBaseModel):
    accessToken: str


class UserRead(UserBase):
    id: PrimaryKey
    role: Optional[str] = Field(None, nullable=True)


