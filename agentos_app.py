"""AgentOS entrypoint. Run with `uv run uvicorn agentos_app:app --reload`."""

import os

from agno.os import AgentOS
from agno.registry import Registry
from dotenv import load_dotenv

from agents.megas_o import MEGAS_O_MODEL, megas_o
from db import DB
from schemas.backlog import Backlog, BacklogItem, OpenQuestion
from schemas.brief import FeatureRequest, ProjectBrief

load_dotenv()

registry = Registry(
    name="Megas-xlr Registry",
    models=[MEGAS_O_MODEL],
    dbs=[DB],
    schemas=[ProjectBrief, FeatureRequest, Backlog, BacklogItem, OpenQuestion],
)

agent_os = AgentOS(
    id="megas-xlr",
    description="Megas-xlr — multi-agent software engineering company (Phase 0)",
    agents=[megas_o],
    db=DB,
    registry=registry,
)

app = agent_os.get_app()


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "agentos_app:app",
        host=os.environ.get("AGENTOS_HOST", "0.0.0.0"),
        port=int(os.environ.get("AGENTOS_PORT", "7777")),
        reload=True,
    )
