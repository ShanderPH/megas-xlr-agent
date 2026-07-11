# ADR-001: CPython 3.14 e política de free-threaded

- Status: aceito
- Data: 2026-07-11

## Decisão

O runtime oficial é CPython `>=3.14,<3.15` convencional, com GIL. Builds free-threaded não são o
runtime padrão e não pertencem à matriz de suporte deste incremento.

## Motivo

Python 3.14 é a baseline aprovada no `plan.md`. O build convencional reduz o risco de extensões
nativas enquanto preserva a opção de benchmark posterior. A suite comprova `Py_GIL_DISABLED != 1`
e `sys._is_gil_enabled()`.

## Consequências

Ambientes, lock, Docker, Ruff, mypy e CI usam 3.14. Windows e Linux executam checks offline. Uma
adoção futura de free-threaded exige benchmark separado de dependências, desempenho e segurança,
além de novo ADR. Recuo para 3.12 exige incompatibilidade central reproduzida e aprovação humana.
