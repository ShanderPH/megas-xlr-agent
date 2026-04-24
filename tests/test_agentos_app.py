import os

import fastapi
import pytest

# Gate the test
pytestmark = pytest.mark.skipif(
    not os.environ.get("GOOGLE_API_KEY"),
    reason="GOOGLE_API_KEY is not set",
)


def test_agentos_app_validity() -> None:
    from agentos_app import agent_os, app

    assert isinstance(app, fastapi.FastAPI)

    # Check if megas_o is in the agents list
    agent_ids = [agent.id for agent in agent_os.agents]
    assert "megas-o" in agent_ids
