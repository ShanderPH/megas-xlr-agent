"""Legacy project brief contracts retained for schema compatibility."""

from pydantic import BaseModel, Field


class ProjectBrief(BaseModel):
    """The stable identity of a project. Changes rarely."""

    name: str = Field(..., description="Human-readable project name, e.g. 'BR Masters'")
    slug: str = Field(..., description="Stable slug for id prefixes, e.g. 'br-masters'")
    domain: str = Field(..., description="Business domain in one sentence")
    tech_stack: list[str] = Field(default_factory=list)
    constraints: list[str] = Field(
        default_factory=list,
        description="Non-negotiable constraints: locales, compliance, performance, etc.",
    )
    target_users: str = Field(default="", description="Who this software serves")
    repo_path: str | None = Field(
        default=None,
        description="Absolute path to the project repo on disk, if available",
    )


class FeatureRequest(BaseModel):
    """A single feature to design a backlog for."""

    title: str = Field(..., max_length=120)
    description: str
    business_goal: str | None = None
    success_metric: str | None = None
