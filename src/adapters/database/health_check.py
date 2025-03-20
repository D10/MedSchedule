from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from .session import get_session


async def db_health_check(session: AsyncSession) -> None:
    try:
        await session.execute(text("SELECT 1"))
    except Exception as exc:
        raise Exception(
            f"ошибка подключения к базе данных {session.bind.engine.url}"
        ) from exc


async def check_database() -> None:
    async with get_session() as session:  # type:ignore[attr-defined]
        await db_health_check(session)
