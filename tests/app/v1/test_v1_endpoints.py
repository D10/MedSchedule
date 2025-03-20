from typing import AsyncGenerator

import pytest
from fastapi import FastAPI
from starlette.testclient import TestClient

from tests.factories import UserFactory

API_PATH = "/api/v1"


@pytest.mark.asyncio
async def test_create_schedule(app: FastAPI, client: TestClient, db_session: AsyncGenerator) -> None:
    user = UserFactory.create()

    response = client.post(
        API_PATH + "/schedule",
        json={
          "medicine_name": "some_name",
          "periodicity_hours": 1,
          "duration_days": 1,
          "user_id": 2
        }
    )

    assert response.status_code == 200


@pytest.mark.asyncio
async def test_get_user_schedules(app: FastAPI, client: TestClient, db_session: AsyncGenerator) -> None:
    response = client.get(API_PATH + "/schedules", params={"user_id": 1})
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_get_user_schedule(app: FastAPI, client: TestClient, db_session: AsyncGenerator) -> None:
    response = client.get(API_PATH + "/schedule", params={"user_id": 1, "schedule_id": 1})
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_get_schedule_with_next_takings(app: FastAPI, client: TestClient, db_session: AsyncGenerator) -> None:
    response = client.get(API_PATH + "/next_takings", params={"user_id": 1})
    assert response.status_code == 200
