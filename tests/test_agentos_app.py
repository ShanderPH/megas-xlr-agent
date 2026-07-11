import fastapi
import pytest


def test_agentos_app_validity_without_credentials(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("GOOGLE_API_KEY", raising=False)
    from agentos_app import create_agent_os, create_app

    agent_os = create_agent_os()
    app = create_app(agent_os)
    assert isinstance(app, fastapi.FastAPI)

    # Check if megas_o is in the agents list
    agent_ids = [agent.id for agent in agent_os.agents]
    assert "megas-o" in agent_ids
