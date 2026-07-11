"""Postgres database construction without opening a connection at import time."""

import os

from agno.db.postgres import PostgresDb

DEFAULT_LOCAL_URL = "postgresql+psycopg://megas:megas_local_dev@localhost:5433/megas_xlr"


def create_db(db_url: str | None = None) -> PostgresDb:
    return PostgresDb(
        db_url=db_url or os.environ.get("DATABASE_URL", DEFAULT_LOCAL_URL),
        id="megas-xlr-db",
    )
