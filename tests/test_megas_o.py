import os
import re

import pytest

# Gate the test
pytestmark = [
    pytest.mark.online,
    pytest.mark.slow,
    pytest.mark.skipif(not os.environ.get("GOOGLE_API_KEY"), reason="GOOGLE_API_KEY is not set"),
]


@pytest.mark.asyncio
async def test_megas_o_smoke() -> None:
    from agents import megas_o
    from schemas.backlog import Backlog
    from scripts.smoke_test import BRIEF, FEATURE

    prompt = (
        "ProjectBrief:\n"
        + BRIEF.model_dump_json(indent=2)
        + "\n\nFeatureRequest:\n"
        + FEATURE.model_dump_json(indent=2)
    )

    result = await megas_o.arun(prompt)
    backlog = result.content

    assert isinstance(backlog, Backlog)
    assert len(backlog.items) >= 8

    layers = {item.layer for item in backlog.items}
    assert {"UI", "Backend", "Database", "Integration", "QA"}.issubset(layers)

    priorities = {item.priority for item in backlog.items}
    assert "P0" in priorities

    assert len(backlog.open_questions) >= 1

    for item in backlog.items:
        assert re.match(r"^BR-LINEUP-\d{3}$", item.id)
