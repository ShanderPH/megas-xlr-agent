"""AgentOS entrypoint. Run with `uv run uvicorn agentos_app:app --reload`."""

import os

from agno.os import AgentOS
from dotenv import load_dotenv

from agents import megas_o

load_dotenv()

agent_os = AgentOS(
    description="Megas-xlr — multi-agent software engineering company (Phase 0)",
    agents=[megas_o],
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
