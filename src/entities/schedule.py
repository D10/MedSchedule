import datetime as dt
from typing import List

from src.entities._base import Entity


class ScheduleEntity(Entity):
    id: int
    user_id: int
    medicine_name: str
    duration_days: int
    periodicity_hours: int
    created_at: dt.datetime


class ScheduleCreateRequestEntity(Entity):
    medicine_name: str
    periodicity_hours: int
    duration_days: int
    user_id: int


class ScheduleIdEntity(Entity):
    id: int


class TakingEntity(Entity):
    date: dt.date
    time: dt.time


class ScheduleWithTakingsEntity(ScheduleEntity):
    takings: List[TakingEntity] | None = None
