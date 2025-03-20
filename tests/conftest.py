from typing import AsyncGenerator

import pytest
import pytest_asyncio
from fastapi import FastAPI
from sqlalchemy import NullPool, create_engine
from sqlalchemy.ext.asyncio import (AsyncSession, async_sessionmaker,
                                    create_async_engine)
from sqlalchemy.orm import sessionmaker
from starlette.testclient import TestClient

from src.adapters.database.models import BaseModel
from src.adapters.database.session import get_scoped_session
from src.app.app import init_app
from src.config.config import settings

TEST_DATABASE_URL = settings.depends.database.test_url

test_engine = create_async_engine(TEST_DATABASE_URL, echo=True, poolclass=NullPool)

test_sync_engine = create_engine(TEST_DATABASE_URL, echo=True, poolclass=NullPool)

test_session_factory = async_sessionmaker(
    bind=test_engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
)

test_sync_session_factory = sessionmaker(
    bind=test_sync_engine,
    autocommit=False,
    expire_on_commit=False,
)

pytest_plugins = ("pytest_asyncio",)


@pytest.fixture
def app() -> FastAPI:
    yield init_app()


@pytest.fixture
def client(app) -> TestClient:
    yield TestClient(app)


@pytest_asyncio.fixture(scope="session")
async def create_test_database() -> None:
    async with test_engine.begin() as conn:
        await conn.run_sync(BaseModel.metadata.create_all)
        await conn.commit()
    yield
    async with test_engine.begin() as conn:
        await conn.run_sync(BaseModel.metadata.drop_all)
        await conn.commit()


@pytest.fixture(scope="session")
async def db_session(create_test_database) -> AsyncGenerator[AsyncSession, None]:
    async with get_scoped_session(test_session_factory) as session:
        yield session
        await session.close()
