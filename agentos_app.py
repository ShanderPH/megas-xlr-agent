"""AgentOS entrypoint with side-effect-free dependency construction."""

import os

from agno.os import AgentOS
from agno.registry import Registry
from fastapi import FastAPI

from agents.megas_o import create_megas_o
from db import create_db
from schemas.backlog import Backlog, BacklogItem, OpenQuestion
from schemas.brief import FeatureRequest, ProjectBrief


def create_agent_os() -> AgentOS:
    db = create_db()
    agent, model = create_megas_o(db)
    registry = Registry(
        name="Megas-xlr Registry",
        models=[model],
        dbs=[db],
        schemas=[ProjectBrief, FeatureRequest, Backlog, BacklogItem, OpenQuestion],
    )
    return AgentOS(
        id="megas-xlr",
        description="Megas-xlr multi-agent engineering system",
        agents=[agent],
        db=db,
        registry=registry,
    )


def create_app(agent_os_instance: AgentOS | None = None) -> FastAPI:
    return (agent_os_instance or create_agent_os()).get_app()


agent_os = create_agent_os()
app = create_app(agent_os)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "agentos_app:app",
        host=os.environ.get("AGENTOS_HOST", "0.0.0.0"),
        port=int(os.environ.get("AGENTOS_PORT", "7777")),
        reload=True,
    )
