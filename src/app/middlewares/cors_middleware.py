from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware as StarletteCorsMiddleware

from src.config.config import settings


class CORSMiddleware(StarletteCorsMiddleware):
    def __init__(self, app: FastAPI):
        super().__init__(
            app,
            allow_origins=settings.serving.http.v1.allowed_origins,
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )
