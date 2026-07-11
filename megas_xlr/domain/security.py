from datetime import UTC, datetime
from enum import StrEnum
from uuid import UUID

from pydantic import BaseModel


class Scope(StrEnum):
    PROJECT_READ = "project:read"
    ARTIFACT_READ = "artifact:read"
    ARTIFACT_WRITE = "artifact:write"
    REPO_METADATA = "repo:metadata"
    GITHUB_READ = "github:read"
    GITHUB_PR_WRITE = "github:pr:write"
    CI_READ = "ci:read"
    TOOL_LOCAL_WRITE = "tool:local-write"
    EXTERNAL_WRITE = "external-write"
    DEPLOY = "deploy"
    SECRETS = "secrets"


def require_scopes(granted: set[Scope], required: set[Scope]) -> None:
    missing = required - granted
    if missing:
        raise PermissionError(f"missing scopes: {','.join(sorted(missing))}")


class ApprovalStatus(StrEnum):
    PENDING = "pending"
    APPROVED = "approved"
    DENIED = "denied"
    EXPIRED = "expired"


class Approval(BaseModel):
    approval_id: UUID
    action: str
    requested_by: str
    expires_at: datetime
    status: ApprovalStatus = ApprovalStatus.PENDING

    def effective_status(self, now: datetime | None = None) -> ApprovalStatus:
        instant = now or datetime.now(UTC)
        if self.status is ApprovalStatus.PENDING and instant >= self.expires_at:
            return ApprovalStatus.EXPIRED
        return self.status
