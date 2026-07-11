# Threat model — Foundation

## Assets and boundaries

Assets are identities, short-lived internal tokens, project/repository scopes, approvals, artifacts,
audit records, budgets and provider credentials. Repository source stays local by default. FastAPI,
the worker, Postgres, GitHub OAuth and future model providers are separate trust boundaries.

## Primary threats and controls

- Stolen authorization codes: OAuth state, PKCE, redirect allowlist and server-side exchange.
- Excessive authority: deny by default, explicit scopes, no deploy scope in the MVP and expiring
  approvals for external writes.
- Replay/duplicate effects: idempotency keys, transactional outbox, leases and completion records.
- Secret/source leakage: structured redaction before audit or traces; source fields denied by default.
- SSRF/egress abuse: future external adapters must use explicit destination allowlists.
- Prompt injection: repository, issue and web content are untrusted data, never policy instructions.
- Budget abuse: soft pause, hard cap and kill switches by capability/provider/project.

## Residual risks

OAuth token exchange and encrypted durable credential storage require deployment key management and
remain disabled until infrastructure is selected. No public exposure is approved by this increment.

