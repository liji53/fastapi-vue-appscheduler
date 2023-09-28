from fastapi import APIRouter, status
from fastapi.responses import JSONResponse

from .schemas import UserRead, UserLogin, UserLoginResponse
from .service import get_user_by_name

from ..core.database import DbSession

auth_router = APIRouter()


@auth_router.get("/me", response_model=UserRead)
def get_me():
    # return {"username": "liki", "id": 1111, "email": "liji37951@hundsun.com"}
    return JSONResponse(status_code=404, content={"a": 1})


@auth_router.post("/login", response_model=UserLoginResponse)
def login_user(user_in: UserLogin, db_session: DbSession):
    user = get_user_by_name(db_session=db_session, username=user_in.username)
    if user and user.check_password(user_in.password):
        return {"accessToken": user.token}

    return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content={"detail": [{"msg": "未认证!"}]})
    # raise ValidationError(
    #     [
    #         ErrorWrapper(
    #             InvalidUsernameError(msg="Invalid username."),
    #             loc="username",
    #         ),
    #         ErrorWrapper(
    #             InvalidPasswordError(msg="Invalid password."),
    #             loc="password",
    #         ),
    #     ],
    #     model=UserLogin,
    # )
