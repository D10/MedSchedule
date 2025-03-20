import uvicorn

from src.config.config import settings


def run_asgi() -> None:
    uvicorn.run(
        "src.app.app:app",
        host=settings.serving.http.v1.addr.host,
        port=settings.serving.http.v1.addr.port,
        reload=settings.debug,
        workers=settings.serving.http.v1.workers,
        log_config=None,
        lifespan="on",
    )


if __name__ == "__main__":
    run_asgi()
