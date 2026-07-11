# Megas-xlr

Sistema multiagente de engenharia baseado em Agno 2.x. A baseline oficial usa CPython 3.14
convencional, com GIL; free-threaded não é suportado como runtime padrão.

## Instalação

```bash
uv python install 3.14
uv sync --all-groups --python 3.14
```

## Execução

Copie `.env.example` para `.env` apenas para uso online. A aplicação pode ser importada e construída
sem `GOOGLE_API_KEY`. Inicie Postgres e a API com `make up` e `make dev`.

## Validação

- `make check`: Ruff, mypy strict, formatação em modo check e testes offline; não altera arquivos.
- `make format`: formata arquivos.
- `make fix`: aplica autofix e formatação.
- `make test-integration`: testa o Postgres local.
- `make clean`: remove apenas caches e relatórios; preserva containers e volumes.
- `CONFIRM_DESTROY_LOCAL_DATA=yes make destroy-local-data`: destrói explicitamente o volume local.

Markers registrados: `offline`, `integration`, `online`, `slow` e `destructive`. A CI executa os
checks offline em Python 3.14 no Windows e Linux. Veja [ADR-001](docs/adr/ADR-001-python-314.md).
