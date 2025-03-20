from typing import AsyncGenerator

import pytest

from src.entities.schedule import ScheduleCreateRequestEntity
from src.services.schedule_service import ScheduleService
from tests.factories import ScheduleFactory, UserFactory


@pytest.mark.asyncio
async def test_create_schedule(db_session: AsyncGenerator) -> None:
    async for session in db_session:
        user = UserFactory.create()
        schedule_request_entity = ScheduleCreateRequestEntity(
            medicine_name="some_med",
            periodicity_hours=1,
            duration_days=1,
            user_id=user.id,
        )
        schedule_id = await ScheduleService.create_schedule(
            session, schedule_request_entity
        )
        assert schedule_id


@pytest.mark.asyncio
async def test_get_user_schedules(db_session: AsyncGenerator) -> None:
    async for session in db_session:
        schedule = ScheduleFactory.create()

        user_schedules = await ScheduleService.get_user_schedules(
            session=session, user_id=schedule.user.id
        )

        assert user_schedules
        assert len(user_schedules) == 1


@pytest.mark.asyncio
async def test_get_user_schedule(db_session: AsyncGenerator) -> None:
    async for session in db_session:
        schedule = ScheduleFactory.create()

        user_schedule = await ScheduleService.get_user_schedule(
            session=session, user_id=schedule.user.id, schedule_id=schedule.id
        )

        assert user_schedule
        assert user_schedule.user_id == schedule.user.id
