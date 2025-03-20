import asyncio
import logging

from sqlalchemy.ext.asyncio import AsyncSession

from src.adapters.database.models import User
from src.adapters.database.session import get_scoped_session, session_factory

logger = logging.getLogger(__name__)

USERS_DATA = [
    {"name": "Жираф"},
    {"name": "Слон"},
    {"name": "Капибара"},
]


async def create_users(session: AsyncSession):
    users = [User(**data) for data in USERS_DATA]
    session.add_all(users)
    await session.commit()


async def main():
    async with get_scoped_session(session_factory) as session:
        await create_users(session)
        logger.info("Наполнение тестовыми данными завершено")


if __name__ == "__main__":
    asyncio.run(main())
