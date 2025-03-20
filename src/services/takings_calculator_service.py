import datetime as dt
from typing import List

from sqlalchemy import Column

from src.config.config import settings
from src.entities.schedule import TakingEntity


class TakingsCalculator:
    DAY_START: dt.time
    DAY_END: dt.time

    def __init__(self) -> None:
        self.DAY_START = self.prepare_time(settings.service.day_start)
        self.DAY_END = self.prepare_time(settings.service.day_end)

    @staticmethod
    def prepare_time(time_str) -> dt.time:
        return dt.datetime.strptime(time_str, "%H:%M").time()

    @staticmethod
    def round_minutes_to_15(time: dt.datetime) -> dt.datetime:
        minutes = ((time.minute // 15) + 1) * 15

        if minutes == 60:
            time += dt.timedelta(hours=1)
            minutes = 0

        return time.replace(minute=minutes, second=0, microsecond=0)

    def adjust_time_to_day_range(
        self,
        time: dt.datetime,
    ) -> dt.datetime:
        today = time.date()

        start_datetime = dt.datetime.combine(today, self.DAY_START)
        end_datetime = dt.datetime.combine(today, self.DAY_END)

        if time < start_datetime:
            result_time = start_datetime
        elif time > end_datetime:
            result_time = start_datetime + dt.timedelta(days=1)
        else:
            result_time = time

        return result_time

    def format_time(
        self,
        time: dt.datetime,
    ):
        time = self.adjust_time_to_day_range(time)
        time = self.round_minutes_to_15(time)
        return time

    def get_schedule_of_takings(
        self,
        periodicity: int | Column[int],
        current_time: dt.datetime,
    ) -> List[TakingEntity]:
        schedule_of_takings = []

        schedule_time = self.format_time(current_time)
        current_date = schedule_time.date()
        end_time = dt.datetime.combine(current_date, self.DAY_END)

        schedule_of_takings.append(
            TakingEntity(
                date=current_date,
                time=schedule_time.time(),
            )
        )

        while schedule_time + dt.timedelta(hours=float(periodicity)) <= end_time:
            next_period = (schedule_time + dt.timedelta(hours=float(periodicity)))

            schedule_of_takings.append(
                TakingEntity(
                    date=current_date,
                    time=next_period.time(),
                )
            )

            schedule_time = next_period

        return schedule_of_takings

    def get_nearest_takings(
        self,
        periodicity: int | Column[int],
        current_time: dt.datetime,
    ) -> List[TakingEntity]:
        schedule_of_takings = self.get_schedule_of_takings(
            periodicity, dt.datetime.combine(current_time, self.DAY_START)
        )
        start_period = current_time.time()
        nearest_period = (current_time + dt.timedelta(hours=settings.service.next_taking_period_hours)).time()

        return list(filter(lambda x: start_period < x.time <= nearest_period, schedule_of_takings))


takings_calculator = TakingsCalculator()
