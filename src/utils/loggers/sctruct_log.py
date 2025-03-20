import logging

import orjson
import structlog

from src.config.config import settings
from src.enums import LogFormat


def setup_struct_logger() -> None:
    processors = [
        structlog.contextvars.merge_contextvars,
        structlog.processors.add_log_level,
        structlog.processors.format_exc_info,
        structlog.processors.TimeStamper(fmt="iso", utc=True),
    ]
    if settings.logging.log_format == LogFormat.plain:
        logger_factory = structlog.PrintLoggerFactory()
        processors.append(structlog.dev.ConsoleRenderer())
    elif settings.logging.log_format == LogFormat.json:
        logger_factory = structlog.BytesLoggerFactory()  # type: ignore[assignment]
        processors.append(structlog.processors.JSONRenderer(serializer=orjson.dumps))
    else:
        raise NotImplementedError(f"Unknown log format: {settings.logging.log_format}!")

    min_level: int = logging.getLevelName(settings.logging.log_level)
    structlog.configure(
        cache_logger_on_first_use=True,
        wrapper_class=structlog.make_filtering_bound_logger(min_level),
        processors=processors,  # type: ignore[arg-type]
        logger_factory=logger_factory,
    )

    formatter = structlog.stdlib.ProcessorFormatter(
        processors=processors,  # type: ignore[arg-type]
    )
    handler = logging.StreamHandler()
    handler.setFormatter(formatter)
    base_logger = logging.getLogger()
    base_logger.addHandler(handler)
    base_logger.setLevel(min_level)
