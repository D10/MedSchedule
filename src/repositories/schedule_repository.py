from typing import Sequence

from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.adapters.database.models import Schedule


class ScheduleRepository:
    @staticmethod
    async def create_schedule(
        session: AsyncSession,
        medicine_name: str,
        periodicity_hours: int,
        duration_days: int,
        user_id: int,
    ) -> int:
        stmt = insert(Schedule).values(
            medicine_name=medicine_name,
            periodicity_hours=periodicity_hours,
            duration_days=duration_days,
            user_id=user_id,
        )

        result = await session.execute(stmt)
        await session.commit()

        schedule_id = result.inserted_primary_key[0]
        return schedule_id

    @staticmethod
    async def get_schedules_by_user_id(
        session: AsyncSession, user_id: int
    ) -> Sequence[Schedule]:
        stmt = select(Schedule).where(Schedule.user_id == user_id)
        return (await session.scalars(stmt)).all()

    @staticmethod
    async def get_schedule(
        session: AsyncSession, schedule_id: int, user_id: int
    ) -> Schedule | None:
        stmt = select(Schedule).where(
            Schedule.id == schedule_id, Schedule.user_id == user_id
        )
        return await session.scalar(stmt)
