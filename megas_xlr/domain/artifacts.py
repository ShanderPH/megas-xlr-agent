from __future__ import annotations

import hashlib
import json
from datetime import UTC, datetime
from enum import StrEnum
from typing import Any, Self
from uuid import UUID, uuid4

from pydantic import BaseModel, Field


class ArtifactStatus(StrEnum):
    DRAFT = "draft"
    SUBMITTED = "submitted"
    ACCEPTED = "accepted"
    REJECTED = "rejected"
    SUPERSEDED = "superseded"


class RepoSnapshot(BaseModel):
    remote: str | None = None
    branch: str | None = None
    commit_sha: str | None = None
    dirty: bool = False
    hashes: dict[str, str] = Field(default_factory=dict)


class ArtifactEnvelope(BaseModel):
    artifact_id: UUID
    artifact_type: str
    schema_version: str = "1.0"
    status: ArtifactStatus = ArtifactStatus.DRAFT
    created_at: datetime
    created_by: str
    content_hash: str
    payload: dict[str, Any]
    source_artifact_ids: tuple[UUID, ...] = ()
    supersedes_id: UUID | None = None
    repo_snapshot: RepoSnapshot = Field(default_factory=RepoSnapshot)

    @classmethod
    def create(
        cls,
        artifact_type: str,
        payload: dict[str, Any],
        *,
        created_by: str,
        artifact_id: UUID | None = None,
    ) -> Self:
        canonical = json.dumps(payload, sort_keys=True, separators=(",", ":"), default=str)
        return cls(
            artifact_id=artifact_id or uuid4(),
            artifact_type=artifact_type,
            created_at=datetime.now(UTC),
            created_by=created_by,
            content_hash=hashlib.sha256(canonical.encode()).hexdigest(),
            payload=payload,
        )

    def with_status(self, status: ArtifactStatus) -> Self:
        if self.status is ArtifactStatus.ACCEPTED:
            raise ValueError("accepted artifacts are immutable")
        return self.model_copy(update={"status": status})
