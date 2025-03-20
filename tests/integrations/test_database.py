import pytest
import sqlalchemy as sa


@pytest.mark.asyncio
async def test_database_connection(db_session):
    async for session in db_session:
        result = await session.execute(sa.text("SELECT 1"))
        assert result.scalar() == 1
