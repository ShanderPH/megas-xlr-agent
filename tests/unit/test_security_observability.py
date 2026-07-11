from datetime import UTC, datetime

import jwt
from opentelemetry.sdk.trace.export.in_memory_span_exporter import InMemorySpanExporter

from megas_xlr.infrastructure.audit import InMemoryAuditLog
from megas_xlr.infrastructure.telemetry import create_tracer_provider, safe_span_attributes
from megas_xlr.security.oauth import create_github_authorization_request
from megas_xlr.security.tokens import decode_token, issue_token
from megas_xlr.settings import TelemetrySettings


def test_short_lived_internal_token_and_denial_after_expiry() -> None:
    signing_key = "a-secure-test-signing-key-with-32-bytes"
    token = issue_token(
        "user",
        ("project:read",),
        issuer="issuer",
        audience="aud",
        signing_key=signing_key,
        ttl_seconds=60,
    )
    assert (
        decode_token(token, issuer="issuer", audience="aud", signing_key=signing_key).sub == "user"
    )
    expired = jwt.encode(
        {"sub": "user", "iss": "issuer", "aud": "aud", "iat": 1, "exp": 2, "scopes": []},
        signing_key,
        algorithm="HS256",
    )
    try:
        decode_token(expired, issuer="issuer", audience="aud", signing_key=signing_key)
    except jwt.ExpiredSignatureError:
        pass
    else:
        raise AssertionError("expired token was accepted")


def test_github_oauth_uses_state_and_pkce() -> None:
    request = create_github_authorization_request("client", "http://localhost/callback")
    assert request.state and request.verifier
    assert "code_challenge_method=S256" in request.authorization_url


def test_audit_and_telemetry_redact_secrets_and_source() -> None:
    audit = InMemoryAuditLog()
    event = audit.append("denied", "user", {"token": "secret", "code": "private"})
    assert event.metadata == {"token": "[REDACTED]", "code": "[REDACTED]"}
    exporter = InMemorySpanExporter()
    provider = create_tracer_provider(TelemetrySettings(enabled=True), exporter)
    tracer = provider.get_tracer("test")
    with tracer.start_as_current_span("request") as span:
        for key, value in safe_span_attributes({"token": "secret", "run.id": "1"}).items():
            span.set_attribute(key, value)
    attributes = exporter.get_finished_spans()[0].attributes
    assert attributes["token"] == "[REDACTED]"
    assert datetime.now(UTC)
