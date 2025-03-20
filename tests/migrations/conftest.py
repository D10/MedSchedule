from argparse import Namespace

import pytest
from alembic.config import Config

from tests.migrations.utils import make_alembic_config


@pytest.fixture()
def alembic_config(postgres_url) -> Config:
    cmd_options = Namespace(
        config="alembic.ini",
        name="alembic",
        pg_url=postgres_url,
        raiseerr=False,
        x=None,
    )
    return make_alembic_config(cmd_options)
