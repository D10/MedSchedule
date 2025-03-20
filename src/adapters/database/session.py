import asyncio
from contextlib import asynccontextmanager
from typing import AsyncGenerator

import structlog
from sqlalchemy.ext.asyncio import (AsyncSession, async_scoped_session,
                                    async_sessionmaker, create_async_engine)
from sqlalchemy.pool import NullPool

from src.config.config import settings

logger = structlog.getLogger(__name__)

engine = create_async_engine(
    settings.depends.database.url,
    poolclass=NullPool,
    echo=settings.debug,
)

session_factory = async_sessionmaker(
    bind=engine,
    expire_on_commit=False,
    autoflush=False,
    class_=AsyncSession,
)


@asynccontextmanager
async def get_scoped_session(
    factory: async_sessionmaker,
) -> AsyncGenerator[AsyncSession, None]:
    scoped_factory = async_scoped_session(
        session_factory=factory,
        scopefunc=asyncio.current_task,
    )
    try:
        async with scoped_factory() as session:
            logger.debug("сессия инициализирована")
            yield session
        logger.debug("сессия закрыта")
    finally:
        await scoped_factory.remove()
        logger.debug("сессия удалена из скоупа")


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with get_scoped_session(session_factory) as session:
        yield session
