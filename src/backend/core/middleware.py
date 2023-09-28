from uuid import uuid1
from contextvars import ContextVar
from typing import Optional
from loguru import logger

from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from fastapi.responses import Response
from fastapi.requests import Request
from sqlalchemy.orm import scoped_session, sessionmaker

from .database import engine

# 每个请求的唯一ID
_request_id_var: ContextVar[Optional[str]] = ContextVar("request_id", default=None)


def get_request_id() -> Optional[str]:
    return _request_id_var.get()


class DBSessionMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        request_id = str(uuid1())
        # 在同一个请求中，使用同一个session
        ctx_token = _request_id_var.set(request_id)
        try:
            session = scoped_session(sessionmaker(bind=engine), scopefunc=get_request_id)
            request.state.db = session()
            response = await call_next(request)
        except Exception as e:
            raise e from None
        finally:
            request.state.db.close()

        _request_id_var.reset(ctx_token)
        return response
