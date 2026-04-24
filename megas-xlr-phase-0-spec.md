# Megas-xlr · Phase 0 — Autonomous Implementation Spec

**Prepared by:** Megas-o (Product + Program orchestrator)
**Executor:** Gemini 3.1 Pro, running inside Antigravity's Agent workspace
**Repository:** `github.com/ShanderPH/megas-xlr-agent` (already initialized, empty)
**Estimated duration:** 2–4 working days with 3 HITL checkpoints
**Author of this spec owns all WHY questions. The executor owns WHAT and HOW.**

---

## 0. Mission

You are acting as a **Senior Platform Engineer**. Your mission is to scaffold the Megas-xlr multi-agent engineering system end-to-end for Phase 0. You work autonomously — plan, create files, run commands, verify, commit, open PR — and stop only at the three HITL checkpoints listed in §12 or when the Definition of Done in §13 is satisfied.

Success is binary: either every item in §13 passes, or Phase 0 is not done. Do not negotiate partial completion.

---

## 1. Why this matters

Megas-xlr is a multi-agent system where six specialist agents (Megas-o, Megas-d, Megas-as, Megas-fs, Megas-qa, Megas-ops) collaborate to turn feature requests into shippable software. It is the **decision and memory layer** of a software engineering company. Code execution is deliberately delegated to external IDE agents (Antigravity, Claude Code, Codex CLI, opencode) via MCP in later phases.

Phase 0 delivers the scaffold plus **Megas-o only**, because Megas-o is the entry point: every future feature passes through his backlog generation step. If Megas-o is wrong, the whole system is wrong.

The other five agents will be added in Phase 1. Do not create logic for them in Phase 0 beyond empty stubs.

---

## 2. Architectural shape (for context)

```
User (Felipe) ─┬─> Antigravity / Claude Code / Codex / opencode  [execution]
               │                   │
               │                MCP (Phase 3, not now)
               │                   ▼
               └─────────> Agno AgentOS (FastAPI @ :7777)
                                   │
                           ┌───────┼───────────┐
                           ▼       ▼           ▼
                        Megas-o  ...other...  stubs
                           │
                           ▼
                      PostgresDb (pgvector)
```

In Phase 0 only the two bold pieces exist: **AgentOS runtime** and **Megas-o agent**. Everything else is either a stub or deferred.

---

## 3. Scope of Phase 0

### 3.1 In scope

1. Python 3.12 project bootstrapped with `uv`.
2. Docker Compose running Postgres 16 with `pgvector` extension.
3. Agno AgentOS running on `localhost:7777`, serving the AgentOS UI.
4. Megas-o agent fully implemented with Gemini 3.1 Pro, calibrated system prompt, Pydantic `output_schema = Backlog`, persistence in Postgres.
5. Pydantic schemas: `ProjectBrief`, `FeatureRequest`, `BacklogItem`, `OpenQuestion`, `Backlog`.
6. Empty stub files for the other five agents with a TODO comment and a failing `NotImplementedError` — so that Phase 1 is just "fill the stub".
7. Smoke test `scripts/smoke_test.py` that feeds the BR Masters lineup brief (§8.1) to Megas-o and validates the output against §8.3 assertions.
8. Pytest test suite with at least: schema round-trip tests, Megas-o smoke test (§8), AgentOS app import test.
9. Pre-commit hooks: ruff (lint + format), mypy (types).
10. `README.md`, `AGENTS.md`, `Makefile`, `.env.example`.
11. First PR opened: branch `feature/phase-0-scaffold` → `main`, with DoD checklist in the description.

### 3.2 Explicitly out of scope for Phase 0

- MCP server exposing AgentOS (Phase 3).
- Actual MCP clients in IDEs (Phase 3).
- Full implementation of Megas-d, Megas-as, Megas-fs, Megas-qa, Megas-ops (Phase 1).
- Team + Workflow orchestration (Phase 2).
- Pinecone actual data upload — init the client skeleton but do not embed anything.
- Authentication/JWT on AgentOS — run in local unauthenticated mode.
- CI/CD (Phase 4).
- Deployment to any cloud.
- Any UI outside the AgentOS built-in Control Plane.
- Any integration with HubSpot, N8N, Heimdall, or InChurch systems. **Megas-xlr is fully isolated from those.**

---

## 4. Hard constraints

| Constraint | Value | Non-negotiable because |
|---|---|---|
| Python version | `>=3.12,<3.13` | Agno 2.x min version + typing features used in schemas |
| Package manager | `uv` | Speed; lockfile discipline; matches JUDAH convention |
| Agno | `>=2.5,<3.0` | Phase 0 uses AgentOS runtime introduced in 2.x |
| Pydantic | `>=2.9,<3.0` | v1 syntax is rejected in this repo |
| Postgres | 16 with pgvector | Aligns with Supabase stack Felipe uses elsewhere |
| Model for Megas-o | `gemini-3.1-pro-preview` via Google AI Studio | User-provided quota; best reasoning/cost ratio as of April 2026 |
| Structured output | `output_schema=Backlog` on the Agent | Contract enforcement; no prose-parsing |
| Commit style | Conventional Commits | `feat:`, `chore:`, `docs:`, `test:`, `refactor:` |
| Line length | 100 chars (ruff) | Matches JUDAH/BR Masters convention |
| Type checking | `mypy --strict` on `agents/`, `schemas/`, `agentos_app.py` | Strictness pays back compound interest |
| Secrets | Only in `.env`; never commit | `.env` in `.gitignore` from commit zero |

If any constraint conflicts with current Agno API (docs.agno.com), **halt and ask** — do not silently downgrade.

---

## 5. Directory structure

Exact layout you will produce. No extra files, no missing files.

```
megas-xlr-agent/
├── .env.example
├── .gitignore
├── .pre-commit-config.yaml
├── .python-version                  # "3.12"
├── AGENTS.md
├── Makefile
├── README.md
├── docker-compose.yml
├── pyproject.toml
├── uv.lock                          # generated by `uv sync`
├── agentos_app.py
├── agents/
│   ├── __init__.py
│   ├── megas_o.py                   # IMPLEMENTED
│   ├── megas_d.py                   # stub
│   ├── megas_as.py                  # stub
│   ├── megas_fs.py                  # stub
│   ├── megas_qa.py                  # stub
│   ├── megas_ops.py                 # stub
│   └── prompts/
│       ├── megas_o.md               # full system prompt
│       └── README.md                # "one prompt per agent, keep < 2000 tokens"
├── schemas/
│   ├── __init__.py                  # re-exports
│   ├── brief.py
│   └── backlog.py
├── scripts/
│   └── smoke_test.py
├── tests/
│   ├── __init__.py
│   ├── conftest.py
│   ├── test_schemas.py
│   ├── test_megas_o.py
│   └── test_agentos_app.py
└── .antigravity/
    └── workspace.json               # optional; helps future Antigravity sessions pick up context
```

Do not create `__init__.py` files I did not list. Do not add folders like `src/` or `app/`. The repo root is the package root — `agents`, `schemas` are packages.

---

## 6. File-by-file specification

### 6.1 `pyproject.toml`

```toml
[project]
name = "megas-xlr-agent"
version = "0.1.0"
description = "Megas-xlr — multi-agent software engineering company. Phase 0 scaffold."
readme = "README.md"
requires-python = ">=3.12,<3.13"
authors = [{ name = "Felipe Braat", email = "felipe@febrate.com" }]
license = { text = "MIT" }
dependencies = [
    "agno>=2.5,<3.0",
    "pydantic>=2.9,<3.0",
    "pydantic-settings>=2.6",
    "fastapi>=0.115",
    "uvicorn[standard]>=0.32",
    "psycopg[binary]>=3.2",
    "sqlalchemy>=2.0",
    "google-genai>=0.8",
    "httpx>=0.27",
    "python-dotenv>=1.0",
]

[dependency-groups]
dev = [
    "pytest>=8.3",
    "pytest-asyncio>=0.24",
    "pytest-cov>=5.0",
    "ruff>=0.7",
    "mypy>=1.13",
    "pre-commit>=4.0",
]

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[tool.hatch.build.targets.wheel]
packages = ["agents", "schemas"]

[tool.ruff]
line-length = 100
target-version = "py312"

[tool.ruff.lint]
select = ["E", "F", "I", "N", "UP", "B", "SIM", "RUF"]
ignore = ["E501"]   # handled by formatter

[tool.ruff.format]
quote-style = "double"

[tool.mypy]
python_version = "3.12"
strict = true
files = ["agents", "schemas", "agentos_app.py"]
plugins = ["pydantic.mypy"]

[tool.pytest.ini_options]
asyncio_mode = "auto"
testpaths = ["tests"]
addopts = "-v --tb=short --strict-markers"
```

Verify with `uv sync && uv run python -c "import agno; print(agno.__version__)"`.

### 6.2 `docker-compose.yml`

```yaml
services:
  postgres:
    image: pgvector/pgvector:pg16
    container_name: megas-xlr-postgres
    restart: unless-stopped
    environment:
      POSTGRES_USER: megas
      POSTGRES_PASSWORD: megas_local_dev
      POSTGRES_DB: megas_xlr
    ports:
      - "5433:5432"          # 5433 to avoid collision with JUDAH/BR Masters local DBs
    volumes:
      - megas_xlr_pg_data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U megas -d megas_xlr"]
      interval: 5s
      timeout: 3s
      retries: 10

volumes:
  megas_xlr_pg_data:
```

Verify with `docker compose up -d && docker compose ps` — Postgres must show `healthy`.

### 6.3 `.env.example`

```dotenv
# Megas-xlr Phase 0 environment
# Copy to .env and fill. Never commit .env.

# Google Gemini — used by Megas-o
GOOGLE_API_KEY=your_google_ai_studio_key_here
GEMINI_MODEL=gemini-3.1-pro-preview

# Reserved for later phases — leave empty or placeholder in Phase 0
ANTHROPIC_API_KEY=
OPENAI_API_KEY=

# Postgres (matches docker-compose.yml)
DATABASE_URL=postgresql+psycopg://megas:megas_local_dev@localhost:5433/megas_xlr

# AgentOS
AGENTOS_HOST=0.0.0.0
AGENTOS_PORT=7777
AGENTOS_LOG_LEVEL=INFO

# Pinecone (skeleton only in Phase 0)
PINECONE_API_KEY=
PINECONE_ENVIRONMENT=
PINECONE_INDEX=megas-xlr-memory
```

### 6.4 `.gitignore`

Standard Python `.gitignore` plus: `.env`, `.env.*`, `!.env.example`, `uv.lock` stays tracked, `.venv/`, `.pytest_cache/`, `.mypy_cache/`, `.ruff_cache/`, `__pycache__/`, `*.pyc`, `.coverage`, `htmlcov/`, `.antigravity/*` except `.antigravity/workspace.json`, `.idea/`, `.vscode/settings.json` (but keep `.vscode/extensions.json` if any), `.DS_Store`.

### 6.5 `.pre-commit-config.yaml`

```yaml
repos:
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.7.4
    hooks:
      - id: ruff
        args: [--fix]
      - id: ruff-format
  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.13.0
    hooks:
      - id: mypy
        additional_dependencies: [pydantic>=2.9]
        args: [--strict]
        files: ^(agents|schemas|agentos_app\.py)
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v5.0.0
    hooks:
      - id: end-of-file-fixer
      - id: trailing-whitespace
      - id: check-yaml
      - id: check-toml
      - id: check-added-large-files
        args: [--maxkb=500]
```

After creating, run `uv run pre-commit install` — must exit zero.

### 6.6 `Makefile`

```makefile
.PHONY: install up down dev test smoke lint typecheck check clean logs

install:
	uv sync --all-groups
	uv run pre-commit install

up:
	docker compose up -d
	@echo "Waiting for Postgres to be healthy..."
	@until docker compose ps postgres | grep -q "healthy"; do sleep 1; done
	@echo "Postgres ready."

down:
	docker compose down

dev: up
	uv run uvicorn agentos_app:app --reload --host $${AGENTOS_HOST:-0.0.0.0} --port $${AGENTOS_PORT:-7777}

test:
	uv run pytest

smoke:
	uv run python scripts/smoke_test.py

lint:
	uv run ruff check . --fix
	uv run ruff format .

typecheck:
	uv run mypy

check: lint typecheck test
	@echo "All checks passed."

clean:
	docker compose down -v
	rm -rf .pytest_cache .mypy_cache .ruff_cache __pycache__ **/__pycache__ .coverage htmlcov

logs:
	docker compose logs -f postgres
```

### 6.7 `README.md`

One page. Sections:
1. **What is this** (2 sentences)
2. **Phase status** (currently "Phase 0 — scaffold + Megas-o MVP")
3. **Quickstart** (`make install` → `make up` → copy `.env.example` to `.env` → `make dev`)
4. **Verify** (run `make check && make smoke`; expected output shape)
5. **Repo layout** (tree)
6. **Roadmap** (link to the phase docs you will generate later; stub for now)
7. **Conventions** (conventional commits, branch naming, PR flow)

No marketing language. No emojis. ≤200 lines total.

### 6.8 `AGENTS.md`

This file is read by Codex CLI, opencode, Claude Code, and Antigravity. It encodes project conventions for any future IDE agent that touches this repo.

```markdown
# Megas-xlr — Repository conventions for IDE agents

## Who reads this
Any AI coding agent (Claude Code, Codex CLI, opencode, Antigravity, Cursor, Windsurf) that operates inside this repo MUST read this file before making changes.

## Project identity
Megas-xlr is a multi-agent engineering system built on Agno 2.x. It is NOT a web app. Do not introduce frontend code, marketing pages, or user-facing HTML unless explicitly asked.

## Hard rules

- Python 3.12 only. Never introduce syntax requiring 3.13+.
- Pydantic v2 syntax only. `Field(default_factory=...)` for mutable defaults. No `.dict()` calls — use `.model_dump()`.
- Agno imports canonical:
  - `from agno.agent import Agent`
  - `from agno.os import AgentOS`
  - `from agno.models.google import Gemini`
  - `from agno.models.anthropic import Claude`
  - `from agno.db.postgres import PostgresDb`
- Every agent has an `output_schema` set to a Pydantic model. No free-form text agents.
- Every new agent gets its system prompt as a standalone `.md` file under `agents/prompts/` — never inline the prompt in Python.
- Never commit to `main` directly. Always branch `feature/*`, `fix/*`, or `chore/*`.
- Never `git push --force` on shared branches.
- Never run `docker compose down -v` without confirming — it nukes Postgres data.
- Never add dependencies without updating `pyproject.toml` AND running `uv sync`.
- `Megas-xlr` MUST remain isolated from InChurch systems (HubSpot, N8N, Heimdall, Jira, Salomão). Never import tools that connect to those.

## Style

- Commits: Conventional Commits. Present tense, lowercase after the colon.
- Line length 100 chars. Double quotes.
- Type hints mandatory on public functions. `-> None` when void.
- Docstrings only where behavior is non-obvious. Do not paraphrase function names.
- Tests live under `tests/`, mirror the package structure.

## When you change behavior
1. Update or add the test first.
2. Implement.
3. Run `make check` locally. If it fails, you are not done.
4. Update `README.md` or `AGENTS.md` if conventions shifted.
5. Open PR against `main` with DoD checklist referenced.

## When you are stuck
Stop. Write a comment in the PR or session describing exactly: (a) what you tried, (b) what failed, (c) what decision Felipe needs to make. Do not guess business rules.

## Multi-project awareness
This agent system serves multiple projects — today BR Masters, tomorrow anything else. Never bake project-specific logic into an agent's system prompt. Project context arrives at runtime via the `ProjectBrief` schema.
```

### 6.9 `schemas/__init__.py`

```python
from schemas.backlog import Backlog, BacklogItem, Layer, OpenQuestion, Priority
from schemas.brief import FeatureRequest, ProjectBrief

__all__ = [
    "Backlog",
    "BacklogItem",
    "FeatureRequest",
    "Layer",
    "OpenQuestion",
    "Priority",
    "ProjectBrief",
]
```

### 6.10 `schemas/brief.py`

```python
"""Inputs that arrive at Megas-o for any project/feature cycle."""

from pydantic import BaseModel, Field


class ProjectBrief(BaseModel):
    """The stable identity of a project. Changes rarely."""

    name: str = Field(..., description="Human-readable project name, e.g. 'BR Masters'")
    slug: str = Field(..., description="Stable slug for id prefixes, e.g. 'br-masters'")
    domain: str = Field(..., description="Business domain in one sentence")
    tech_stack: list[str] = Field(default_factory=list)
    constraints: list[str] = Field(
        default_factory=list,
        description="Non-negotiable constraints: locales, compliance, performance, etc.",
    )
    target_users: str = Field(default="", description="Who this software serves")
    repo_path: str | None = Field(
        default=None,
        description="Absolute path to the project repo on disk, if available",
    )


class FeatureRequest(BaseModel):
    """A single feature to design a backlog for."""

    title: str = Field(..., max_length=120)
    description: str
    business_goal: str | None = None
    success_metric: str | None = None
```

### 6.11 `schemas/backlog.py`

```python
"""The structured output Megas-o produces."""

from typing import Literal

from pydantic import BaseModel, Field, field_validator

Priority = Literal["P0", "P1", "P2"]
Layer = Literal["UI", "Backend", "Database", "Integration", "QA", "DevOps", "Documentation"]


class BacklogItem(BaseModel):
    id: str = Field(
        ...,
        description="Slug-style id: <PROJECT-SLUG>-<FEATURE-SLUG>-<NNN>. Stable across runs.",
    )
    title: str = Field(..., max_length=80)
    description: str
    layer: Layer
    priority: Priority
    acceptance_criteria: list[str] = Field(..., min_length=2)
    dependencies: list[str] = Field(
        default_factory=list,
        description="IDs of other items that must ship first",
    )
    estimate_hours: float = Field(..., ge=0.5, le=40.0)

    @field_validator("id")
    @classmethod
    def id_is_upper_slug(cls, v: str) -> str:
        if not v.replace("-", "").isalnum() or v != v.upper():
            raise ValueError("id must be UPPER-CASE slug like 'BR-LINEUP-001'")
        return v


class OpenQuestion(BaseModel):
    question: str
    blocks: list[str] = Field(
        default_factory=list,
        description="BacklogItem ids that cannot proceed without this answer",
    )


class Backlog(BaseModel):
    project: str
    feature: str
    summary: str = Field(..., description="One-sentence restatement of what will be built")
    items: list[BacklogItem] = Field(..., min_length=1)
    open_questions: list[OpenQuestion] = Field(default_factory=list)
    estimated_total_hours: float = Field(..., ge=0.5)

    @field_validator("estimated_total_hours")
    @classmethod
    def total_matches_items(cls, v: float, info) -> float:  # type: ignore[no-untyped-def]
        items = info.data.get("items") or []
        s = sum(i.estimate_hours for i in items)
        if abs(v - s) > 0.5:
            raise ValueError(f"estimated_total_hours ({v}) does not match sum of items ({s})")
        return v
```

### 6.12 `agents/__init__.py`

```python
from agents.megas_o import megas_o

__all__ = ["megas_o"]
```

### 6.13 `agents/prompts/megas_o.md`

This is the full body of Megas-o's system prompt. Write exactly the following content to the file. Do not paraphrase, do not truncate, do not add preambles.

```markdown
# Role

You are Megas-o, the orchestrator of the Megas-xlr multi-agent engineering team. You combine the disciplines of a Senior Product Owner and a Senior Technical Program Manager. You are terse, precise, and useful. You never make project management jokes.

# Mission

Turn a ProjectBrief plus a FeatureRequest into a structured, actionable Backlog that the rest of the team (designer, architect, full-stack lead, QA, DevOps) can execute against. You decide WHAT will be built, for WHOM, with WHICH acceptance criteria, in WHAT priority order. You do not write code. You do not design UIs. You do not decide architecture beyond layering.

# Mental model

When a brief arrives, think in this order:

1. Restate the problem in one sentence. If you cannot, the brief is not ready — raise an OpenQuestion.
2. Identify the primary user and the measurable business goal.
3. Break the feature into 2–4 vertical slices. Each slice must independently deliver user-visible value.
4. For each slice, enumerate backlog items across the relevant layers: UI, Backend, Database, Integration, QA, DevOps, Documentation. Not every slice touches every layer.
5. For each item, write acceptance criteria as "Given ... When ... Then ..." statements. Minimum two per item.
6. Assign priority. P0 = blocks release, P1 = must-have for launch, P2 = post-launch improvement.
7. Encode dependencies by explicit item id. Never rely on implicit ordering.
8. Estimate in hours, conservatively. Any item above 8 hours must be split.
9. Flag ambiguity as an OpenQuestion. Do not invent business rules to keep flow.

# Heuristics you always apply

- External API integrations always produce four items: fetch, cache/rate-limit, failure/retry, cost-monitoring.
- User-facing forms always produce: validation story + error-state UX story.
- New database tables always produce: migration story (with rollback), index/query story.
- Features touching auth, payments, or PII always include a security review story at P1.
- Observability (structured logs, error tracking, key metrics) is P1. Never P2.
- Time-based logic (deadlines, locking, scheduling, cron) always includes a timezone/DST story.
- i18n is P1 when the brief mentions multiple locales, otherwise P2.
- Any destructive user action (delete, lock, submit-final) includes a confirmation UX story and an audit log story.

# Item id format

`<PROJECT-SLUG>-<FEATURE-SLUG>-<NNN>` where:
- PROJECT-SLUG = uppercase slug of the project (e.g. BR for BR Masters)
- FEATURE-SLUG = 2–8 uppercase letters summarizing the feature (e.g. LINEUP)
- NNN = zero-padded sequence

Example: `BR-LINEUP-004`.

# Escalate, do not guess

Use OpenQuestion when:
- A business rule is ambiguous (scoring, pricing, access tiers, time windows).
- The brief implies a third-party integration but does not name provider or tier.
- Multiple alternative UX patterns exist with non-trivial trade-offs.
- Legal or compliance implications appear (LGPD, payment regulation, minors, accessibility law).

Each OpenQuestion lists the item ids it blocks.

# Hard refusals

- You do not invent business rules.
- You do not propose a tech stack. You honor the ProjectBrief.tech_stack.
- You do not produce code, SQL, or UI mockups.
- You do not produce architecture diagrams.
- You do not generate marketing copy or user-facing strings.
- You do not speak outside the Backlog JSON in your final output.

# Multi-project awareness

The ProjectBrief you receive in a given run may be BR Masters today, InChurch Knowledge Base tomorrow, and something else next week. You never bake project-specific assumptions into your behavior. All project context flows through the ProjectBrief schema.

# Output contract

Your final output MUST be a single JSON object matching the `Backlog` schema. The runtime will validate it. No markdown fences. No preamble. No closing remarks. No commentary. Pure JSON.

If you cannot produce a valid Backlog (insufficient brief, missing required fields), return a Backlog with:
- `items`: at least one item of type `Documentation` asking for clarification
- `open_questions`: one OpenQuestion per piece of missing information

Never return an empty items list. Never return prose.
```

### 6.14 `agents/megas_o.py`

```python
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
    agent_id="megas-o",
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
```

If the exact Agno import paths differ in the installed version, consult `docs.agno.com` and adjust — but keep the public symbol `megas_o` as `Agent`-instance.

### 6.15 Stub files for other agents

Each of `agents/megas_d.py`, `agents/megas_as.py`, `agents/megas_fs.py`, `agents/megas_qa.py`, `agents/megas_ops.py` contains:

```python
"""<Agent Name> — <one line role>. IMPLEMENTED IN PHASE 1."""


def _not_implemented() -> None:
    raise NotImplementedError(
        "<agent_id> is scheduled for Phase 1. See megas-xlr-phase-0-spec.md §3.2."
    )
```

Replace `<Agent Name>`, `<one line role>`, and `<agent_id>` per agent:

| File | Agent Name | One-line role | agent_id |
|---|---|---|---|
| megas_d.py | Megas-d | UI/UX designer | megas-d |
| megas_as.py | Megas-as | Software architect | megas-as |
| megas_fs.py | Megas-fs | Fullstack lead and code reviewer | megas-fs |
| megas_qa.py | Megas-qa | QA planner and test strategist | megas-qa |
| megas_ops.py | Megas-ops | DevOps and deploy orchestrator | megas-ops |

### 6.16 `agents/prompts/README.md`

```markdown
# Agent prompts

One markdown file per agent. Keep each under 2000 tokens — short, imperative, hierarchical. Never inline prompts in Python code; load them from here at agent construction time.

Convention: filename = `<agent_id_snake_case>.md`. Example: `megas_o.md`.
```

### 6.17 `agentos_app.py`

```python
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
```

### 6.18 `tests/conftest.py`

```python
"""Shared pytest fixtures."""

from pathlib import Path

import pytest
from dotenv import load_dotenv


@pytest.fixture(scope="session", autouse=True)
def _load_env() -> None:
    env_path = Path(__file__).parent.parent / ".env"
    if env_path.exists():
        load_dotenv(env_path)
```

### 6.19 `tests/test_schemas.py`

Required assertions:
1. `Backlog.model_validate(...)` round-trips with a minimal fixture (1 item, 0 open questions).
2. `BacklogItem.id` rejects lowercase: `"br-lineup-001"` raises `ValidationError`.
3. `BacklogItem.acceptance_criteria` with one entry raises `ValidationError` (min 2 required).
4. `Backlog.estimated_total_hours` mismatch by >0.5 raises `ValidationError`.
5. `BacklogItem.estimate_hours` accepts 0.5, rejects 0.4 and 41.

### 6.20 `tests/test_agentos_app.py`

Required assertions:
1. `from agentos_app import app` imports without exception.
2. `app` is a FastAPI instance (`isinstance(app, fastapi.FastAPI)`).
3. `megas_o` is registered in `agent_os.agents`.
4. This test is gated by an env var check: skip if `GOOGLE_API_KEY` is unset, so CI without secrets does not fail.

### 6.21 `tests/test_megas_o.py`

Marked `@pytest.mark.slow` because it hits Gemini. Skipped if `GOOGLE_API_KEY` is empty.

Asserts:
1. Feeding the BR Masters brief (§8.1) to `megas_o.arun(...)` returns a `Backlog` instance.
2. `len(backlog.items) >= 8`.
3. `{item.layer for item in backlog.items}` is a superset of `{"UI", "Backend", "Database", "Integration", "QA"}`.
4. At least one `item.priority == "P0"` exists.
5. At least one `OpenQuestion` is present (because the brief is deliberately under-specified on scoring rules).
6. Every item id matches regex `^BR-LINEUP-\d{3}$`.

### 6.22 `scripts/smoke_test.py`

Human-runnable smoke. Produces console output; does not assert. Prints the full Backlog JSON so Felipe can eyeball quality.

```python
"""Run Megas-o against the BR Masters lineup brief and print the Backlog JSON."""

import asyncio
import json
from dotenv import load_dotenv

from agents import megas_o
from schemas.brief import FeatureRequest, ProjectBrief

load_dotenv()

BRIEF = ProjectBrief(
    name="BR Masters",
    slug="br-masters",
    domain=(
        "Brazilian football predictions — gamified betting-style picks "
        "for the Brasileirão season"
    ),
    tech_stack=[
        "Next.js 16",
        "TypeScript 5.6",
        "Supabase (Postgres + Auth + Storage)",
        "HeroUI v3",
        "Tailwind CSS v4",
        "Framer Motion",
        "Zod",
        "Mercado Pago SDK",
        "SofaScore API via RapidAPI",
        "HMAC-SHA256 webhook verification",
    ],
    constraints=[
        "Multi-tenant; each user owns their picks",
        "pt-BR primary locale; EN secondary",
        "Must respect Brazilian holidays and timezone (America/Sao_Paulo)",
        "All monetary values in BRL, rounded to cents",
    ],
    target_users=(
        "Brazilian football fans aged 18-45 who want to gamify "
        "their predictions for weekly Brasileirão rounds"
    ),
)

FEATURE = FeatureRequest(
    title="Escalar o time da rodada",
    description=(
        "User selects 11 players (1 GK + 10 outfield in a valid 4-3-3, 4-4-2, "
        "or 3-5-2 tactical formation) for a given round of the Brasileirão. "
        "Players must come from teams playing that round. SofaScore API feeds "
        "fresh lineups, injuries, and suspensions. Users submit before kickoff; "
        "once the round begins, the lineup locks. Scoring is based on real-player "
        "performance during the round — goals, assists, cards, minutes played."
    ),
    business_goal=(
        "Increase weekly active user engagement and session depth "
        "during Brasileirão rounds"
    ),
    success_metric=(
        "At least 60% of active users submit a lineup for each round; "
        "average time-to-submit under 8 minutes"
    ),
)


async def main() -> None:
    prompt = (
        "ProjectBrief:\n"
        + BRIEF.model_dump_json(indent=2)
        + "\n\nFeatureRequest:\n"
        + FEATURE.model_dump_json(indent=2)
    )
    result = await megas_o.arun(prompt)
    backlog = result.content
    print(json.dumps(backlog.model_dump(), indent=2, ensure_ascii=False))


if __name__ == "__main__":
    asyncio.run(main())
```

### 6.23 `.antigravity/workspace.json`

Small file recording the phase and primary agent for Antigravity to pick up context in future sessions:

```json
{
  "project": "megas-xlr-agent",
  "phase": "0",
  "primary_spec": "megas-xlr-phase-0-spec.md",
  "primary_model": "gemini-3.1-pro-preview",
  "conventions": "See AGENTS.md"
}
```

---

## 7. Smoke test — BR Masters lineup feature

### 7.1 Input

Already encoded in `scripts/smoke_test.py` above.

### 7.2 Expected output shape (directional, not a hard contract)

A `Backlog` with roughly:

- 3–5 UI items (formation selector, player picker grid, lineup summary, submit confirmation, locked-state view)
- 3–5 Backend items (lineup persistence endpoint, validation rules, lock scheduler, scoring calculator, user lineup fetch)
- 2–3 Database items (lineups table migration, round_players snapshot table, indexes)
- 3–4 Integration items (SofaScore fetch, players cache, rate-limit handler, cost monitoring)
- 2–3 QA items (formation validation test matrix, lock timing E2E, SofaScore failure simulation)
- 1–2 DevOps items (cron for lock at kickoff, observability dashboard)
- ≥2 Open questions (at minimum: scoring rule specifics, whether re-editing is allowed after submit-before-kickoff, budget/player-cost constraints)

Total: **13–22 items**, estimate total likely 60–100h.

### 7.3 Assertions (what `tests/test_megas_o.py` enforces)

Minimum enforceable:
- ≥ 8 items
- Covers `{UI, Backend, Database, Integration, QA}` at minimum
- At least one P0
- ≥ 1 OpenQuestion
- ID regex pass

If any assertion fails, do not silently tweak the prompt to pass the test. Halt and ask Felipe.

---

## 8. Execution sequence

Execute tasks in this order. Commit after each major task. Do not batch.

1. **chore: init repo config** — `pyproject.toml`, `.gitignore`, `.python-version`, `.env.example`, `.pre-commit-config.yaml`. Run `uv sync --all-groups` → must exit zero.
2. **chore: add docker compose** — `docker-compose.yml`, verify `docker compose up -d` → Postgres healthy.
3. **chore: add Makefile and docs** — `Makefile`, `README.md`, `AGENTS.md`.
4. **feat: add schemas** — `schemas/brief.py`, `schemas/backlog.py`, `schemas/__init__.py`. Run `uv run mypy schemas/` → zero errors.
5. **feat: add megas-o prompt** — `agents/prompts/megas_o.md`, `agents/prompts/README.md`.
6. **feat: add megas-o agent** — `agents/megas_o.py`, `agents/__init__.py`, all stub files.
7. **feat: add AgentOS app** — `agentos_app.py`. Run `uv run uvicorn agentos_app:app` → starts without error. Open `http://localhost:7777` → AgentOS UI shows Megas-o.
8. **test: add schemas tests** — `tests/test_schemas.py`. `uv run pytest tests/test_schemas.py` → green.
9. **test: add agentos app test** — `tests/test_agentos_app.py`. Green.
10. **test: add megas-o smoke test** — `tests/test_megas_o.py` and `scripts/smoke_test.py`. Run the smoke. **HITL CHECKPOINT #2 (see §9)**.
11. **chore: add antigravity workspace** — `.antigravity/workspace.json`.
12. **Open PR** — branch `feature/phase-0-scaffold` → `main`. PR description uses the DoD (§10) as a checklist. **HITL CHECKPOINT #3**.

---

## 9. HITL checkpoints

You stop and wait for Felipe's reply at exactly these three points. Do not proceed until he writes "continue" (or equivalent).

**Checkpoint 1 — After task 4 (schemas committed).**
Post a message with:
- Short summary of what exists
- Any deviations from the spec and why
- The full content of `schemas/brief.py` and `schemas/backlog.py` for review
- Wait.

**Checkpoint 2 — After task 10 (smoke test run).**
Post a message with:
- The full `Backlog` JSON that Megas-o produced for the BR Masters brief
- A self-assessment against §8.3 assertions
- Any warning the smoke produced (latency, token count, etc.)
- Wait. Felipe either approves or tweaks the system prompt.

**Checkpoint 3 — PR opened.**
Post the PR URL, the full CI-equivalent output of `make check && make smoke`, and the DoD checklist (§10) with every box explicitly ticked or marked "n/a with reason". Wait for merge approval.

---

## 10. Definition of Done for Phase 0

Every box must be checked before declaring Phase 0 complete.

- [ ] `uv sync --all-groups` installs cleanly in a fresh venv.
- [ ] `docker compose up -d` → `postgres` healthy within 30 seconds.
- [ ] `uv run uvicorn agentos_app:app --reload` starts on :7777 with no errors.
- [ ] AgentOS UI at `http://localhost:7777` lists Megas-o as an available agent.
- [ ] `make check` exits zero (lint + typecheck + tests).
- [ ] `make smoke` prints a valid Backlog JSON for BR Masters with ≥8 items, ≥1 OpenQuestion, and layer coverage ≥ `{UI, Backend, Database, Integration, QA}`.
- [ ] `pre-commit run --all-files` exits zero.
- [ ] `AGENTS.md` exists and matches §6.8 verbatim.
- [ ] `agents/prompts/megas_o.md` matches §6.13 verbatim.
- [ ] PR `feature/phase-0-scaffold` opened against `main` with checklist.
- [ ] No secrets committed (verify with `git log -p | grep -i "api_key\|secret\|token"` returns nothing from your commits).
- [ ] No files outside the directory structure in §5.

---

## 11. Git workflow

- Branch: `feature/phase-0-scaffold` off `main`. Never commit on `main` directly.
- Commit granularity: one commit per task in §9. Never squash before the PR is open.
- Commit messages: Conventional Commits, imperative, present tense, lowercase after colon. Examples:
  - `chore: init uv project and pre-commit config`
  - `feat(schemas): add ProjectBrief, FeatureRequest and Backlog`
  - `feat(agents): add Megas-o with Gemini 3.1 Pro`
  - `test: add Megas-o smoke against BR Masters lineup brief`
- PR title: `feat: Phase 0 scaffold — Megas-o MVP`
- PR body: copy the DoD from §10 as a checklist, plus short "what was tried and worked" and "known follow-ups (Phase 1)".

---

## 12. Escalation protocol

Halt and ask Felipe if:

- An Agno 2.x API import path in §6 does not exist in the installed version and no 1-line fix is obvious.
- `uv sync` fails due to a dependency resolution conflict.
- Gemini 3.1 Pro returns an error that persists after 2 retries with exponential backoff.
- The smoke test output fails §7.3 assertions even after one prompt-tuning iteration.
- You notice the spec is internally inconsistent. Do not silently choose one interpretation.
- Any security-relevant decision (how to store secrets, what to log).

Framing of escalation messages: one paragraph on "what I tried", one on "what failed or is ambiguous", one on "the exact decision I need from you". No hedging, no apologies.

---

## 13. Phase 1 preview (not your job, but keep it compatible)

Phase 1 will: implement the five other agents by filling the stubs with real `Agent(...)` instances using the same pattern as Megas-o, add `team.py` and `workflow.py` files at repo root, and add integration tests. Design your Phase 0 output so Phase 1 is pure addition — no edits to files you created except stub replacement.

Do not pre-optimize for Phase 1. Just do not paint yourself into a corner.

---

## 14. Final instruction to the executor

You have the full spec. Begin with task 1 in §9. Commit often. Halt at the three HITL checkpoints. Be precise about what works and what does not. When in doubt, ask.
