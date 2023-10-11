from fastapi import APIRouter, status
from fastapi.responses import JSONResponse
from loguru import logger

from .schemas import UserRead, UserLogin, UserLoginResponse
from .service import get_user_by_name

from ..core.database import DbSession

auth_router = APIRouter()


@auth_router.post("/login", response_model=UserLoginResponse)
def login(user_in: UserLogin, db_session: DbSession):
    logger.debug(f"登录: {user_in.model_dump()}")
    user = get_user_by_name(db_session=db_session, username=user_in.username)
    if user and user.check_password(user_in.password):
        return {"accessToken": user.token, "username": user.username, "roles": ["admin"],
                "refreshToken": "?", "expires": user.expired}

    return JSONResponse(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, content={"detail": "登录失败!"})
