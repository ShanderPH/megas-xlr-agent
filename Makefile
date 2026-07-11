.PHONY: install up down dev test test-integration lint format fix typecheck check clean destroy-local-data logs
install:
	uv sync --all-groups --python 3.14
up:
	docker compose up -d postgres
down:
	docker compose down
dev: up
	uv run uvicorn agentos_app:app --reload --host 0.0.0.0 --port 7777
test:
	uv run pytest -m "not integration and not online and not slow and not destructive"
test-integration:
	uv run pytest -m integration
lint:
	uv run ruff check .
format:
	uv run ruff format .
fix:
	uv run ruff check . --fix
	uv run ruff format .
typecheck:
	uv run mypy
check: lint typecheck test
	uv run ruff format --check .
clean:
	uv run python scripts/clean.py
destroy-local-data:
	@if [ "$${CONFIRM_DESTROY_LOCAL_DATA}" != "yes" ]; then echo "Refusing; set CONFIRM_DESTROY_LOCAL_DATA=yes"; exit 1; fi
	docker compose down -v
logs:
	docker compose logs -f postgres
