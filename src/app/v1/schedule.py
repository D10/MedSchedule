from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.adapters.database.session import get_session
from src.entities.schedule import (ScheduleCreateRequestEntity,
                                   ScheduleIdEntity, ScheduleWithTakingsEntity)
from src.services.schedule_service import ScheduleService

router = APIRouter(tags=["Schedule"])


@router.post("/schedule", response_model=ScheduleIdEntity)
async def create_schedule(
    schema: ScheduleCreateRequestEntity,
    session: AsyncSession = Depends(get_session),
):
    schedule_id = await ScheduleService.create_schedule(session, schema)
    return {"id": schedule_id}


@router.get("/schedules", response_model=List[int])
async def get_user_schedules(
    user_id: int,
    session: AsyncSession = Depends(get_session),
):
    return await ScheduleService.get_user_schedules(session, user_id)


@router.get("/schedule", response_model=ScheduleWithTakingsEntity)
async def get_user_schedule(
    user_id: int,
    schedule_id: int,
    session: AsyncSession = Depends(get_session),
):
    return await ScheduleService.get_user_schedule(session, user_id, schedule_id)


@router.get("/next_takings", response_model=List[ScheduleWithTakingsEntity])
async def get_schedule_with_next_takings(
    user_id: int,
    session: AsyncSession = Depends(get_session),
):
    return await ScheduleService.get_next_takings_for_user(session, user_id)
