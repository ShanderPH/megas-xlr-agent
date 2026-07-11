import os

import pytest
from alembic import command
from alembic.config import Config
from sqlalchemy import create_engine, inspect


@pytest.mark.integration
def test_migrations_upgrade_and_downgrade() -> None:
    url = os.environ.get(
        "TEST_DATABASE_URL",
        "postgresql+psycopg://megas:megas_local_dev@localhost:5433/megas_xlr",
    )
    engine = create_engine(url)
    config = Config("alembic.ini")
    with engine.begin() as connection:
        config.attributes["connection"] = connection
        command.upgrade(config, "head")
        assert "outbox_events" in inspect(connection).get_table_names()
        command.downgrade(config, "base")
        command.upgrade(config, "head")
    engine.dispose()
