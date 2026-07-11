# Incremento 1 — registro de execução

## Baseline

- `main` atualizada em 2026-07-11 para `0e78fe3`.
- remoção do legado Google GenAI/Megas-o confirmada pelo merge de `1f3b1f8`.
- branch de trabalho: `feature/increment-1-foundation`.

## Divergências registradas antes da implementação

1. O ClickUp descreve o milestone apenas como “Construir domínio, persistência, segurança,
   observabilidade e runtime adaptado”; `plan.md` contém a decomposição canônica 1A–1D e os gates.
2. O ClickUp possui uma task explícita para GitHub OAuth/OIDC, mas não expõe tasks equivalentes para
   toda a granularidade 1A–1D encontrada no plano.
3. `plan.md` ainda menciona preservar Megas-o atrás de flag. A decisão posterior, já mergeada em
   `main`, removeu completamente Google GenAI/Megas-o. O Incremento 1 não restaura o legado.
4. A validação Windows é local. O gate Linux só pode ser comprovado pelo CI e não será declarado
   concluído nesta sessão sem evidência correspondente.

`plan.md` permanece a fonte canônica. Nenhuma divergência amplia o escopo para o Incremento 2.

## Comandos e resultados

- `uv sync --all-groups --python 3.14`: lock atualizado; 76 pacotes resolvidos.
- `uv sync --frozen --all-groups --python 3.14`: aprovado em CPython 3.14.4 convencional.
- `uv run ruff check .`: aprovado.
- `uv run ruff format --check .`: aprovado.
- `uv run mypy`: aprovado em modo strict.
- pytest offline: 25 aprovados, 2 selecionados apenas como integração.
- pytest integration: 2 aprovados contra Postgres real, incluindo downgrade/upgrade Alembic.
- `uv run alembic current`: `0001_foundation (head)`.
- import de `agentos_app`: aprovado sem credenciais e sem conexão antecipada.
- `git diff --check`: aprovado.
- `make` não está instalado no host Windows. Os comandos exatos dos alvos `check` e `clean` foram
  executados individualmente; não alteraram o worktree e preservaram o volume Postgres.

## Ações externas

- ClickUp `868kbdwab` alterado de `to do` para `in progress` após início comprovado.
- Nenhum push, PR, merge, deploy ou publicação foi realizado.
