"""Legacy backlog contracts retained for schema compatibility."""

from typing import Literal

from pydantic import BaseModel, Field, field_validator

Priority = Literal["P0", "P1", "P2"]
Layer = Literal["UI", "Backend", "Database", "Integration", "QA", "DevOps", "Documentation"]


class BacklogItem(BaseModel):
    id: str = Field(
        ...,
        description="Slug-style id: <PROJECT-SLUG>-<FEATURE-SLUG>-<NNN>. Stable across runs.",
    )
    title: str = Field(..., max_length=80)
    description: str
    layer: Layer
    priority: Priority
    acceptance_criteria: list[str] = Field(..., min_length=2)
    dependencies: list[str] = Field(
        default_factory=list,
        description="IDs of other items that must ship first",
    )
    estimate_hours: float = Field(..., ge=0.5, le=40.0)

    @field_validator("id")
    @classmethod
    def id_is_upper_slug(cls, v: str) -> str:
        if not v.replace("-", "").isalnum() or v != v.upper():
            raise ValueError("id must be UPPER-CASE slug like 'BR-LINEUP-001'")
        return v


class OpenQuestion(BaseModel):
    question: str
    blocks: list[str] = Field(
        default_factory=list,
        description="BacklogItem ids that cannot proceed without this answer",
    )


class Backlog(BaseModel):
    project: str
    feature: str
    summary: str = Field(..., description="One-sentence restatement of what will be built")
    items: list[BacklogItem] = Field(..., min_length=1)
    open_questions: list[OpenQuestion] = Field(default_factory=list)
    estimated_total_hours: float = Field(..., ge=0.5)

    @field_validator("estimated_total_hours")
    @classmethod
    def total_matches_items(cls, v: float, info) -> float:  # type: ignore[no-untyped-def]
        items = info.data.get("items") or []
        s = sum(i.estimate_hours for i in items)
        if abs(v - s) > 0.5:
            raise ValueError(f"estimated_total_hours ({v}) does not match sum of items ({s})")
        return v
