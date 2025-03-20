from fastapi import FastAPI

from src.app.lifespan import lifespan
from src.app.middlewares.middlewares import setup_middlewares
from src.app.router import router as api_router
from src.utils.loggers.loggers import setup_logging


def init_app() -> FastAPI:
    setup_logging()
    application = FastAPI(
        title="MedSchedule API",
        lifespan=lifespan,
    )
    setup_middlewares(application)

    application.include_router(api_router)
    return application


app = init_app()
