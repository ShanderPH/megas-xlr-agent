# Megas-xlr

Megas-xlr is a multi-agent engineering system built on Agno 2.x, designed to autonomously plan, architect, and orchestrate software tasks. It acts as the decision and memory layer for software engineering projects.

## Phase status

Phase 0 — scaffold + Megas-o MVP

## Quickstart

1. `make install`
2. `make up`
3. `cp .env.example .env` (fill in your Gemini API key)
4. `make dev`

## Verify

Run the checks and smoke test:

```bash
make check
make smoke
```

The smoke test will output a JSON representation of the generated backlog for the target feature.

## Repo layout

```text
megas-xlr-agent/
├── agentos_app.py
├── agents/          # Megas agents and prompts
├── schemas/         # Pydantic schemas (Brief, Backlog, etc.)
├── scripts/         # Smoke tests and utility scripts
└── tests/           # Pytest test suite
```

## Roadmap

Phase 0 delivers the scaffold plus Megas-o only. See [megas-xlr-phase-0-spec.md](megas-xlr-phase-0-spec.md).

## Conventions

- Use Conventional Commits (`feat:`, `chore:`, etc.)
- Branch naming: `feature/*`, `fix/*`, `chore/*`
- Pull Request flow: Open a PR against `main` with DoD checklist verified before merging.
