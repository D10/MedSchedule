import datetime as dt
from typing import List

from sqlalchemy.ext.asyncio import AsyncSession

from src.entities.schedule import (ScheduleCreateRequestEntity,
                                   ScheduleWithTakingsEntity)
from src.repositories.schedule_repository import ScheduleRepository
from src.services.takings_calculator_service import takings_calculator


class ScheduleService:
    @staticmethod
    async def create_schedule(
        session: AsyncSession,
        schema: ScheduleCreateRequestEntity,
    ) -> int:
        return await ScheduleRepository.create_schedule(
            session=session,
            medicine_name=schema.medicine_name,
            periodicity_hours=schema.periodicity_hours,
            duration_days=schema.duration_days,
            user_id=schema.user_id,
        )

    @staticmethod
    async def get_user_schedules(session: AsyncSession, user_id: int) -> List[int]:
        user_schedules = await ScheduleRepository.get_schedules_by_user_id(
            session=session, user_id=user_id
        )
        return [user_schedule.id for user_schedule in user_schedules]  # type:ignore[misc]

    @staticmethod
    async def get_user_schedule(
        session: AsyncSession,
        user_id: int,
        schedule_id: int,
    ) -> ScheduleWithTakingsEntity | None:
        schedule = await ScheduleRepository.get_schedule(
            session=session, user_id=user_id, schedule_id=schedule_id
        )
        if schedule is None:
            return None
        elif not schedule.is_active:
            return None

        schedule_entity = ScheduleWithTakingsEntity(**schedule.as_dict())
        schedule_takings = takings_calculator.get_schedule_of_takings(
            periodicity=schedule.periodicity_hours,
            current_time=dt.datetime.now()
        )
        schedule_entity.takings = schedule_takings

        return schedule_entity

    @staticmethod
    async def get_next_takings_for_user(
        session: AsyncSession,
        user_id: int,
    ) -> List[ScheduleWithTakingsEntity]:
        schedules_with_takings = []

        current_time = dt.datetime.now()

        schedules = await ScheduleRepository.get_schedules_by_user_id(
            session=session,
            user_id=user_id,
        )

        for schedule in schedules:
            schedule_entity = ScheduleWithTakingsEntity(**schedule.as_dict())
            nearest_takings = takings_calculator.get_nearest_takings(
                current_time=current_time,
                periodicity=schedule.periodicity_hours
            )
            if not nearest_takings or not schedule.is_active:
                continue
            schedule_entity.takings = nearest_takings
            schedules_with_takings.append(schedule_entity)

        return schedules_with_takings
