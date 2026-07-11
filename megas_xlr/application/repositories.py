from typing import Protocol
from uuid import UUID

from megas_xlr.domain.artifacts import ArtifactEnvelope


class ArtifactRepository(Protocol):
    def add(self, artifact: ArtifactEnvelope) -> None: ...
    def get(self, artifact_id: UUID) -> ArtifactEnvelope | None: ...


class InMemoryArtifactRepository:
    def __init__(self) -> None:
        self._artifacts: dict[UUID, ArtifactEnvelope] = {}

    def add(self, artifact: ArtifactEnvelope) -> None:
        if artifact.artifact_id in self._artifacts:
            raise ValueError("artifact already exists")
        self._artifacts[artifact.artifact_id] = artifact

    def get(self, artifact_id: UUID) -> ArtifactEnvelope | None:
        return self._artifacts.get(artifact_id)
