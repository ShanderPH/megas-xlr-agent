import pytest
from pydantic import ValidationError

from megas_xlr.settings import Environment, Settings


def test_settings_have_typed_sections_and_environment_precedence(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("MEGAS_DB__URL", "postgresql+psycopg://env@localhost/env")
    settings = Settings(db={"url": "postgresql+psycopg://init@localhost/init"})
    assert settings.db.url == "postgresql+psycopg://init@localhost/init"
    assert settings.environment is Environment.TEST


def test_production_settings_require_auth_secrets() -> None:
    with pytest.raises(ValidationError):
        Settings(environment="production")
