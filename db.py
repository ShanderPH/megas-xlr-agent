"""Centralized PostgresDb singleton. Every module imports DB from here."""

import os
from pathlib import Path

from agno.db.postgres import PostgresDb
from dotenv import load_dotenv

load_dotenv(Path(__file__).parent / ".env")

_DEFAULT_LOCAL_URL = "postgresql+psycopg://megas:megas_local_dev@localhost:5433/megas_xlr"
_DB_URL = os.environ.get("DATABASE_URL", _DEFAULT_LOCAL_URL)

DB = PostgresDb(db_url=_DB_URL, id="megas-xlr-db")

__all__ = ["DB"]
