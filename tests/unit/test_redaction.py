from megas_xlr.security.redaction import redact


def test_redaction_removes_secrets_and_source_content() -> None:
    value = redact({"authorization": "Bearer secret", "source_code": "print('secret')", "ok": 1})
    assert value == {"authorization": "[REDACTED]", "source_code": "[REDACTED]", "ok": 1}
