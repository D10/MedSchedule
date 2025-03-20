from typing import AsyncGenerator

import pytest

from src.repositories.schedule_repository import ScheduleRepository
from tests.factories import ScheduleFactory


@pytest.mark.asyncio
async def test_create_schedule(db_session: AsyncGenerator) -> None:
    async for session in db_session:
        schedule = await ScheduleFactory.create()

        schedule = await ScheduleRepository.get_schedule(
            session=session,
            schedule_id=schedule.id,
            user_id=schedule.user.id,
        )

        assert schedule
        assert schedule.user_id == schedule.user.id


@pytest.mark.asyncio
async def test_get_schedules_by_user_id(db_session: AsyncGenerator) -> None:
    async for session in db_session:
        schedule = await ScheduleFactory.create()

        user_schedules = await ScheduleRepository.get_schedules_by_user_id(
            session=session,
            user_id=schedule.user.id,
        )

        assert user_schedules
        assert len(user_schedules) == 1
        assert user_schedules[0].user_id == schedule.user.id


@pytest.mark.asyncio
async def test_get_schedule(db_session: AsyncGenerator) -> None:
    async for session in db_session:
        schedule = await ScheduleFactory.create()

        schedule = await ScheduleRepository.get_schedule(
            session=session,
            schedule_id=schedule.id,
            user_id=schedule.user.id,
        )

        assert schedule
        assert schedule.user_id == schedule.user.id
