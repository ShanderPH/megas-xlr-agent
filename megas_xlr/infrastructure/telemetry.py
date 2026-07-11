from collections.abc import Mapping
from typing import Any

from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import SimpleSpanProcessor, SpanExporter

from megas_xlr.security.redaction import redact
from megas_xlr.settings import TelemetrySettings


def create_tracer_provider(
    settings: TelemetrySettings, exporter: SpanExporter | None = None
) -> TracerProvider:
    provider = TracerProvider(resource=Resource.create({"service.name": settings.service_name}))
    if settings.enabled and exporter is not None:
        provider.add_span_processor(SimpleSpanProcessor(exporter))
    return provider


def safe_span_attributes(attributes: Mapping[str, Any]) -> dict[str, Any]:
    redacted = redact(dict(attributes))
    return {
        key: value for key, value in redacted.items() if isinstance(value, str | bool | int | float)
    }
