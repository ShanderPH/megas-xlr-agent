import os

import psycopg
import pytest


@pytest.mark.integration
def test_local_postgres_connection() -> None:
    url = os.environ.get(
        "DATABASE_URL",
        "postgresql://megas:megas_local_dev@localhost:5433/megas_xlr",
    ).replace("postgresql+psycopg://", "postgresql://")
    with psycopg.connect(url, connect_timeout=5) as connection:
        assert connection.execute("SELECT 1").fetchone() == (1,)
