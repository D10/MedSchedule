import asyncio
from logging.config import fileConfig

from alembic import context
from sqlalchemy.ext.asyncio import async_engine_from_config

from src.adapters.database.models.base import BaseModel
from src.config.config import settings

config = context.config
fileConfig(config.config_file_name)  # type:ignore[arg-type]

config.set_main_option("sqlalchemy.url", settings.depends.database.url)
target_metadata = BaseModel.metadata


def run_migrations_offline():
    context.configure(
        url=settings.depends.database.url,
        target_metadata=target_metadata,
        literal_binds=True,
    )
    with context.begin_transaction():
        context.run_migrations()


async def run_migrations_online():
    connectable = async_engine_from_config(
        config.get_section(config.config_ini_section), prefix="sqlalchemy.", future=True
    )

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)


def do_run_migrations(connection):
    context.configure(connection=connection, target_metadata=target_metadata)
    with context.begin_transaction():
        context.run_migrations()


async def main():
    async with async_engine_from_config(
        config.get_section(config.config_ini_section), prefix="sqlalchemy.", future=True
    ).connect() as connection:
        await connection.run_sync(do_run_migrations)


if context.is_offline_mode():
    run_migrations_offline()
else:
    asyncio.run(main())
