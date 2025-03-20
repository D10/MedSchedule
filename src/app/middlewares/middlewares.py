from fastapi import FastAPI

from .cors_middleware import CORSMiddleware
from .struct_log_middleware import StructLogMiddleware


def setup_middlewares(_app: FastAPI) -> None:
    _app.add_middleware(CORSMiddleware)
    _app.add_middleware(StructLogMiddleware)
