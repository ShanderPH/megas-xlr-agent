from fastapi.testclient import TestClient

from megas_xlr.bootstrap import create_application
from megas_xlr.settings import Settings


def test_application_constructs_without_secrets_or_database_connection() -> None:
    app = create_application(Settings())
    with TestClient(app) as client:
        response = client.get("/health/live")
    assert response.status_code == 200
    assert response.json() == {"status": "alive"}
