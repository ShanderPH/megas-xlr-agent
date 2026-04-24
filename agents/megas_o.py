"""Megas-o — Orchestrator agent. Turns briefs into backlogs."""

import os
from pathlib import Path

from agno.agent import Agent
from agno.models.google import Gemini

from db import DB
from schemas.backlog import Backlog

_PROMPT_PATH = Path(__file__).parent / "prompts" / "megas_o.md"
_MODEL_ID = os.environ.get("GEMINI_MODEL", "gemini-3.1-pro-preview")


def _load_instructions() -> str:
    if not _PROMPT_PATH.exists():
        raise RuntimeError(f"Megas-o prompt file missing at {_PROMPT_PATH}")
    return _PROMPT_PATH.read_text(encoding="utf-8")


# Module-level model so agentos_app can register the exact same instance
# in the Registry without tripping over Agent.model being Optional[Model].
MEGAS_O_MODEL: Gemini = Gemini(id=_MODEL_ID)


megas_o = Agent(
    name="Megas-o",
    id="megas-o",
    description=(
        "Orchestrator — Senior Product Owner plus Senior Technical Program Manager. "
        "Turns a ProjectBrief plus FeatureRequest into a structured Backlog."
    ),
    model=MEGAS_O_MODEL,
    instructions=_load_instructions(),
    output_schema=Backlog,
    db=DB,
    markdown=False,
    telemetry=False,
)
