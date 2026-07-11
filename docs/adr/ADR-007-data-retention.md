# ADR-007: classificação, egress e retenção de dados

- Status: aceito
- Data: 2026-07-11

## Decisão

Código-fonte e evidence packs brutos não saem do host por padrão. Upload exige consentimento e TTL de
24 horas. Artefatos aceitos usam retenção padrão de 30 dias; audit metadata sem código, 90 dias;
traces redigidos, 14 dias; métricas agregadas, 90 dias. Valores permanecem configuráveis.

## Consequências

Logs, audit e spans passam por redaction. Exclusão por projeto e storage cifrado são gates antes de
exposição pública. Metadados sincronizados nunca incluem source por padrão.

