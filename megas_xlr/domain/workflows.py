from dataclasses import dataclass, replace
from enum import StrEnum


class WorkflowState(StrEnum):
    REQUESTED = "requested"
    RESEARCHING = "researching"
    RESEARCH_REVIEW = "research_review"
    PLANNING = "planning"
    PLAN_REVIEW = "plan_review"
    IMPLEMENTING = "implementing"
    VERIFYING = "verifying"
    READY_FOR_RELEASE = "ready_for_release"
    RELEASED = "released"
    NEEDS_INPUT = "needs_input"
    FAILED = "failed"
    CANCELLED = "cancelled"


_ALLOWED: dict[WorkflowState, frozenset[WorkflowState]] = {
    WorkflowState.REQUESTED: frozenset({WorkflowState.RESEARCHING, WorkflowState.CANCELLED}),
    WorkflowState.RESEARCHING: frozenset(
        {WorkflowState.RESEARCH_REVIEW, WorkflowState.NEEDS_INPUT}
    ),
    WorkflowState.RESEARCH_REVIEW: frozenset({WorkflowState.PLANNING, WorkflowState.RESEARCHING}),
    WorkflowState.PLANNING: frozenset({WorkflowState.PLAN_REVIEW, WorkflowState.NEEDS_INPUT}),
    WorkflowState.PLAN_REVIEW: frozenset({WorkflowState.IMPLEMENTING, WorkflowState.PLANNING}),
    WorkflowState.IMPLEMENTING: frozenset({WorkflowState.VERIFYING, WorkflowState.PLAN_REVIEW}),
    WorkflowState.VERIFYING: frozenset(
        {WorkflowState.READY_FOR_RELEASE, WorkflowState.IMPLEMENTING}
    ),
    WorkflowState.READY_FOR_RELEASE: frozenset({WorkflowState.RELEASED}),
}


@dataclass(frozen=True)
class WorkflowInstance:
    state: WorkflowState = WorkflowState.REQUESTED
    version: int = 0

    def transition(self, target: WorkflowState, expected_version: int) -> WorkflowInstance:
        if expected_version != self.version:
            raise RuntimeError("optimistic concurrency conflict")
        if target not in _ALLOWED.get(self.state, frozenset()):
            raise ValueError(f"invalid transition: {self.state} -> {target}")
        return replace(self, state=target, version=self.version + 1)
