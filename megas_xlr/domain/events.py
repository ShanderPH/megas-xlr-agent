from typing import Any
from uuid import UUID

from pydantic import BaseModel, Field


class OutboxEvent(BaseModel):
    event_id: UUID
    topic: str
    payload: dict[str, Any] = Field(default_factory=dict)
