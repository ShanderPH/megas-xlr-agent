"""ASGI entrypoint; construction is explicit and connection-free."""

import os

from agno.os import AgentOS
from agno.registry import Registry
from fastapi import FastAPI

from megas_xlr.bootstrap import create_application
from megas_xlr.runtime.agno import create_agent_os as build_agent_os
from megas_xlr.runtime.agno import create_agno_database
from megas_xlr.settings import Settings
from schemas.backlog import Backlog, BacklogItem, OpenQuestion
from schemas.brief import FeatureRequest, ProjectBrief


def create_agent_os(settings: Settings | None = None, base_app: FastAPI | None = None) -> AgentOS:
    resolved = settings or Settings()
    db = create_agno_database(resolved.db.url)
    registry = Registry(
        name="Megas-xlr Registry",
        dbs=[db],
        schemas=[ProjectBrief, FeatureRequest, Backlog, BacklogItem, OpenQuestion],
    )
    return build_agent_os(db, registry, base_app=base_app)


def create_app(
    settings: Settings | None = None, agent_os_instance: AgentOS | None = None
) -> FastAPI:
    resolved = settings or Settings()
    base_app = create_application(resolved)
    return (agent_os_instance or create_agent_os(resolved, base_app)).get_app()


app = create_app()

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "agentos_app:app",
        host=os.environ.get("AGENTOS_HOST", "0.0.0.0"),
        port=int(os.environ.get("AGENTOS_PORT", "7777")),
        reload=True,
    )
