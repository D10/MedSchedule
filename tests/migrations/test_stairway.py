"""
Stairway-тест не требует поддержки и позволяет быстро и дешево находить
огромное количество распространенных типовых ошибок в миграциях:
- не реализованные методы downgrade,
- не удаленные типы данных в методах downgrade (например, enum),
- опечатки и другие ошибки.

Идея теста заключается в том, чтобы накатывать миграции по одной,
последовательно выполняя для каждой миграции методы upgrade, downgrade,
upgrade.

Подробнее про stairway тест можно посмотреть в записи доклада с Moscow
Python: https://bit.ly/3bpJ0gw
"""

import pytest
from alembic.command import downgrade, upgrade
from alembic.config import Config
from alembic.script import Script, ScriptDirectory
from sqlalchemy import Connection

from tests.conftest import test_engine


def get_revisions(config) -> list[Script]:
    # Получаем директорию с миграциями alembic
    revisions_dir = ScriptDirectory.from_config(config)
    # Получаем миграции и сортируем в порядке от первой до последней
    revisions = list(revisions_dir.walk_revisions("base", "heads"))
    revisions.reverse()
    return revisions


@pytest.mark.order(1)
async def test_migrations_stairway() -> None:
    async with test_engine.begin() as connection:
        await connection.run_sync(apply_alembic_migrations)


def apply_alembic_migrations(connection: Connection) -> None:
    config = Config(file_="alembic.ini", attributes={"connection": connection})
    config.set_main_option("script_location", "src/migrations/schema")
    for revision in get_revisions(config):
        upgrade(config, revision.revision)
        # -1 используется для downgrade первой миграции (т.к. ее down_revision
        # равен None)
        downgrade(config, revision.down_revision or "-1")
        upgrade(config, revision.revision)
