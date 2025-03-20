import uuid

import structlog
from starlette.middleware.base import (BaseHTTPMiddleware,
                                       RequestResponseEndpoint)
from starlette.requests import Request
from starlette.responses import Response

from src.utils.request_url import get_endpoint_from_request


class StructLogMiddleware(BaseHTTPMiddleware):
    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        endpoint = get_endpoint_from_request(request)
        structlog.contextvars.clear_contextvars()
        structlog.contextvars.bind_contextvars(
            method=request.method,
            request_id=str(uuid.uuid4()),
            endpoint=endpoint,
        )
        response = await call_next(request)
        return response
