from typing import Optional
from .models import User


def get_user_by_name(*, db_session, username: str) -> Optional[User]:
    return db_session.query(User).filter(User.username == username).one_or_none()
