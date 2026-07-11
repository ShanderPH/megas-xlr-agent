from typing import Any

from agno.db.postgres import PostgresDb
from agno.os import AgentOS
from agno.registry import Registry


class AgnoRuntimeAdapter:
    def __init__(self, agent_os: AgentOS) -> None:
        self._agent_os = agent_os

    def run(self, capability: str, input_data: dict[str, Any]) -> dict[str, Any]:
        raise LookupError(f"capability is not registered: {capability}")


def create_agno_database(db_url: str) -> PostgresDb:
    return PostgresDb(db_url=db_url, id="megas-xlr-agno-db")


def create_agent_os(db: PostgresDb, registry: Registry, *, base_app: Any = None) -> AgentOS:
    return AgentOS(
        id="megas-xlr",
        description="Megas-xlr multi-agent engineering system",
        agents=[],
        db=db,
        registry=registry,
        base_app=base_app,
    )
