from typing import Optional

from .models import User
from .schemas import UserRegister


def get_user_by_name(*, db_session, username: str) -> Optional[User]:
    return db_session.query(User).filter(User.username == username).one_or_none()


def create_user(*, db_session, user_in: UserRegister) -> User:
    user = User(**user_in.model_dump())
    db_session.add(user)
    db_session.commit()
    return user
