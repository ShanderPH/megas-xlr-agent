from datetime import UTC, datetime, timedelta
from uuid import uuid4

from megas_xlr.domain.events import OutboxEvent
from megas_xlr.infrastructure.outbox.memory import InMemoryOutbox


def test_outbox_recovers_expired_lease_without_duplicate_effect() -> None:
    outbox = InMemoryOutbox()
    event = OutboxEvent(event_id=uuid4(), topic="test", payload={"id": 1})
    outbox.add(event)
    first = outbox.lease("worker-1", datetime.now(UTC), timedelta(seconds=1))
    assert first == [event]
    recovered = outbox.lease(
        "worker-2", datetime.now(UTC) + timedelta(seconds=2), timedelta(seconds=1)
    )
    assert recovered == [event]
    assert outbox.complete(event.event_id, "worker-2")
    assert outbox.complete(event.event_id, "worker-2")
    assert outbox.pending_count == 0
