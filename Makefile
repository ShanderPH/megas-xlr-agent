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
