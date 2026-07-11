from dataclasses import dataclass
from datetime import datetime, timedelta
from uuid import UUID

from megas_xlr.domain.events import OutboxEvent


@dataclass
class _Entry:
    event: OutboxEvent
    leased_by: str | None = None
    lease_until: datetime | None = None
    completed: bool = False


class InMemoryOutbox:
    def __init__(self) -> None:
        self._entries: dict[UUID, _Entry] = {}

    def add(self, event: OutboxEvent) -> None:
        self._entries.setdefault(event.event_id, _Entry(event))

    def lease(self, worker: str, now: datetime, duration: timedelta) -> list[OutboxEvent]:
        leased: list[OutboxEvent] = []
        for entry in self._entries.values():
            expired = entry.lease_until is not None and entry.lease_until <= now
            if not entry.completed and (entry.leased_by is None or expired):
                entry.leased_by = worker
                entry.lease_until = now + duration
                leased.append(entry.event)
        return leased

    def complete(self, event_id: UUID, worker: str) -> bool:
        entry = self._entries[event_id]
        if entry.completed:
            return True
        if entry.leased_by != worker:
            return False
        entry.completed = True
        return True

    @property
    def pending_count(self) -> int:
        return sum(not entry.completed for entry in self._entries.values())
