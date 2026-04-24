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
