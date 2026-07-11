from datetime import UTC, datetime
from typing import Any
from uuid import UUID, uuid4

from pydantic import BaseModel, Field

from megas_xlr.security.redaction import redact


class AuditEvent(BaseModel):
    event_id: UUID = Field(default_factory=uuid4)
    event_type: str
    actor: str
    metadata: dict[str, Any]
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))


class InMemoryAuditLog:
    def __init__(self) -> None:
        self._events: list[AuditEvent] = []

    def append(self, event_type: str, actor: str, metadata: dict[str, Any]) -> AuditEvent:
        event = AuditEvent(event_type=event_type, actor=actor, metadata=redact(metadata))
        self._events.append(event)
        return event

    @property
    def events(self) -> tuple[AuditEvent, ...]:
        return tuple(self._events)
