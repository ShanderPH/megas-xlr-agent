"""Megas-o agent factory."""

import os
from pathlib import Path

from agno.agent import Agent
from agno.db.postgres import PostgresDb
from agno.models.google import Gemini

from schemas.backlog import Backlog

PROMPT_PATH = Path(__file__).parent / "prompts" / "megas_o.md"


def load_instructions() -> str:
    if not PROMPT_PATH.exists():
        raise RuntimeError(f"Megas-o prompt file missing at {PROMPT_PATH}")
    return PROMPT_PATH.read_text(encoding="utf-8")


def create_megas_o(db: PostgresDb) -> tuple[Agent, Gemini]:
    model = Gemini(id=os.environ.get("GEMINI_MODEL", "gemini-3.1-pro-preview"))
    agent = Agent(
        name="Megas-o",
        id="megas-o",
        description="Orchestrator that turns a project brief into a structured backlog.",
        model=model,
        instructions=load_instructions(),
        output_schema=Backlog,
        db=db,
        markdown=False,
        telemetry=False,
    )
    return agent, model
