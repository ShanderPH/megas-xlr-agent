from datetime import UTC, datetime, timedelta
from decimal import Decimal
from uuid import uuid4

import pytest

from megas_xlr.domain.artifacts import ArtifactEnvelope, ArtifactStatus
from megas_xlr.domain.budgets import Budget, BudgetExceededError
from megas_xlr.domain.security import Approval, ApprovalStatus, Scope, require_scopes
from megas_xlr.domain.workflows import WorkflowInstance, WorkflowState


def test_artifact_hash_is_deterministic_and_accepted_artifact_is_immutable() -> None:
    envelope = ArtifactEnvelope.create("test", {"b": 2, "a": 1}, created_by="user")
    same = ArtifactEnvelope.create(
        "test", {"a": 1, "b": 2}, created_by="user", artifact_id=envelope.artifact_id
    )
    assert envelope.content_hash == same.content_hash
    accepted = envelope.with_status(ArtifactStatus.ACCEPTED)
    with pytest.raises(ValueError, match="immutable"):
        accepted.with_status(ArtifactStatus.REJECTED)


def test_scope_denial_and_approval_expiry() -> None:
    with pytest.raises(PermissionError):
        require_scopes({Scope.PROJECT_READ}, {Scope.ARTIFACT_WRITE})
    approval = Approval(
        approval_id=uuid4(),
        action="external-write",
        requested_by="user",
        expires_at=datetime.now(UTC) - timedelta(seconds=1),
    )
    assert approval.effective_status(datetime.now(UTC)) is ApprovalStatus.EXPIRED


def test_budget_hard_cap_is_enforced() -> None:
    budget = Budget(soft_limit=Decimal("1"), hard_limit=Decimal("2"))
    with pytest.raises(BudgetExceededError):
        budget.charge(Decimal("2.01"))


def test_workflow_transitions_are_versioned_and_deterministic() -> None:
    workflow = WorkflowInstance().transition(WorkflowState.RESEARCHING, expected_version=0)
    assert workflow.version == 1
    with pytest.raises(RuntimeError, match="concurrency"):
        workflow.transition(WorkflowState.RESEARCH_REVIEW, expected_version=0)
    with pytest.raises(ValueError, match="invalid transition"):
        workflow.transition(WorkflowState.RELEASED, expected_version=1)
