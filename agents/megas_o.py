"""Megas-o — Orchestrator agent. Turns briefs into backlogs."""

import os
from pathlib import Path

from agno.agent import Agent
from agno.db.postgres import PostgresDb
from agno.models.google import Gemini

from schemas.backlog import Backlog

_PROMPT_PATH = Path(__file__).parent / "prompts" / "megas_o.md"
_DB_URL = os.environ.get(
    "DATABASE_URL",
    "postgresql+psycopg://megas:megas_local_dev@localhost:5433/megas_xlr",
)
_MODEL_ID = os.environ.get("GEMINI_MODEL", "gemini-3.1-pro-preview")


def _load_instructions() -> str:
    if not _PROMPT_PATH.exists():
        raise RuntimeError(f"Megas-o prompt file missing at {_PROMPT_PATH}")
    return _PROMPT_PATH.read_text(encoding="utf-8")


megas_o = Agent(
    name="Megas-o",
    id="megas-o",
    description=(
        "Orchestrator — Senior Product Owner plus Senior Technical Program Manager. "
        "Turns a ProjectBrief plus FeatureRequest into a structured Backlog."
    ),
    model=Gemini(id=_MODEL_ID),
    instructions=_load_instructions(),
    output_schema=Backlog,
    db=PostgresDb(db_url=_DB_URL),
    markdown=False,
    telemetry=False,
)
