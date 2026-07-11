"""Shared pytest fixtures."""

import pytest


@pytest.fixture(autouse=True)
def _isolate_environment(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("MEGAS_ENVIRONMENT", "test")
