import datetime as dt
from typing import AsyncGenerator

import pytest

from src.services.takings_calculator_service import takings_calculator
from tests.factories import ScheduleFactory


@pytest.mark.parametrize(
    "str_time, expected_result",
    [
        ("08:30", dt.time(8, 30)),
        ("15:26", dt.time(15, 26)),
        ("00:00", dt.time(0, 0)),
    ]
)
def test_prepare_time(str_time: str, expected_result: dt.time) -> None:
    prepared_time = takings_calculator.prepare_time(str_time)
    assert prepared_time == expected_result


@pytest.mark.parametrize(
    "time, expected_result",
    [
        (
            dt.datetime(2024, 8, 12, 8, 7),
            dt.datetime(2024, 8, 12, 8, 15)
        ),
        (
            dt.datetime(2024, 8, 12, 10, 25),
            dt.datetime(2024, 8, 12, 10, 30)
        ),
        (
            dt.datetime(2024, 8, 12, 17, 55),
            dt.datetime(2024, 8, 12, 18, 00)
        )
    ]
)
def test_round_minutes_to_15(time: dt.datetime, expected_result: dt.datetime) -> None:
    rounded_datetime = takings_calculator.round_minutes_to_15(time)
    assert rounded_datetime == expected_result


@pytest.mark.parametrize(
    "time, expected_result",
    [
        (
            dt.datetime(2024, 8, 12, 3, 7),
            dt.datetime(2024, 8, 12, takings_calculator.DAY_START.hour, takings_calculator.DAY_START.minute),
        ),
        (
            dt.datetime(2024, 8, 12, 23, 59),
            dt.datetime(2024, 8, 13, takings_calculator.DAY_START.hour, takings_calculator.DAY_START.minute)
        ),
        (
            dt.datetime(2024, 8, 12, 13, 12),
            dt.datetime(2024, 8, 12, 13, 12)
        ),
    ]
)
def test_adjust_time_to_day_range(time: dt.datetime, expected_result: dt.datetime) -> None:
    adjusted_time = takings_calculator.adjust_time_to_day_range(time)
    assert adjusted_time == expected_result


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "periodicity, quantity_takings",
    [
        (1, 14),
        (2, 7),
        (3, 4)
    ]
)
async def test_get_schedule_of_takings(periodicity: int, quantity_takings: int, db_session: AsyncGenerator) -> None:
    async for session in db_session:
        schedule = await ScheduleFactory.create(periodicity_hours=periodicity)

        schedule_of_takings = takings_calculator.get_schedule_of_takings(
            periodicity=schedule.periodicity_hours,
            current_time=dt.datetime.now(),
        )

        assert len(schedule_of_takings) == quantity_takings


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "periodicity, quantity_takings",
    [
        (1, 1),
        (12, 0),
        (6, 1)
    ]
)
async def test_get_nearest_takings(periodicity: int, quantity_takings: int, db_session: AsyncGenerator) -> None:
    async for session in db_session:
        schedule = await ScheduleFactory.create(periodicity_hours=periodicity)

        current_time = dt.datetime(2025, 8, 24, 12, 15)

        nearest_takings = takings_calculator.get_nearest_takings(
            schedule.periodicity_hours,
            current_time=current_time,
        )
        assert len(nearest_takings) == quantity_takings
