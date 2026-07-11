# ADR-003: Agno atrás de port e critérios de saída

- Status: aceito
- Data: 2026-07-11

## Decisão

Agno 2.x permanece apenas no adapter `megas_xlr.runtime.agno`. Domínio e aplicação dependem de
`AgentRuntime` e `ModelGateway`, sem tipos Agno. Nenhum provider/modelo concreto é selecionado na
Foundation.

## Critérios objetivos de saída

Substituir Agno será proposto quando ao menos um destes critérios for reproduzido: impossibilidade de
structured output exigido; efeitos de import/conexão inevitáveis; falha de isolamento entre projetos;
ausência de recovery/idempotência necessária; bloqueio de tracing/redaction; incompatibilidade com o
runtime Python aprovado; ou custo operacional mensuravelmente superior a um adapter alternativo.

A saída exige contract tests equivalentes, migration de sessões documentada, benchmark, rollback e
aprovação humana. Preferência de fornecedor isolada não é critério.

