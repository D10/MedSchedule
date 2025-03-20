import os
from argparse import Namespace
from pathlib import Path

from alembic.config import Config

PROJECT_PATH = Path(__file__).parent.parent.parent.resolve()


def make_alembic_config(
    cmd_opts: Namespace, base_path: os.PathLike = PROJECT_PATH
) -> Config:
    if not os.path.isabs(cmd_opts.config):
        cmd_opts.config = os.path.join(base_path, cmd_opts.config)

    config = Config(file_=cmd_opts.config, ini_section=cmd_opts.name, cmd_opts=cmd_opts)

    alembic_location = config.get_main_option("script_location")
    assert alembic_location is not None
    if not os.path.isabs(alembic_location):
        config.set_main_option(
            "script_location", os.path.join(base_path, alembic_location)
        )
    if cmd_opts.pg_url:
        config.set_main_option("sqlalchemy.url", cmd_opts.pg_url)

    return config
