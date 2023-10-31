from datetime import datetime, timedelta

from jose import jwt
from loguru import logger
from fastapi.security.utils import get_authorization_scheme_param

from ..core.config import JWT_EXP, JWT_SECRET, JWT_ALG, JWT_REFRESH_TOKEN_EXP


def get_token(username, refresh=False):
    now = datetime.now()
    if not refresh:
        exp = (now + timedelta(seconds=JWT_EXP)).timestamp()
    else:
        exp = (now + timedelta(seconds=JWT_REFRESH_TOKEN_EXP)).timestamp()
    data = {
        "exp": exp,
        "username": username,
    }
    return jwt.encode(data, JWT_SECRET, algorithm=JWT_ALG)


def decode_token(token_in: str):
    scheme, token = get_authorization_scheme_param(token_in)
    if scheme.lower() != "bearer":
        logger.error("refresh_token非法")
        return

    try:
        # jwt会自动校验是否过期
        data = jwt.decode(token, JWT_SECRET, algorithms=JWT_ALG)
    except Exception as e:
        logger.error(f"jwt 解码失败. 原因：{e}")
        return

    return data


def expired():
    now = datetime.now()
    exp = (now + timedelta(seconds=JWT_EXP)).strftime("%Y/%m/%d %H:%M:%S")
    return exp
