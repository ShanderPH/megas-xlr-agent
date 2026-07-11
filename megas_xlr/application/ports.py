from typing import Any, Protocol

from pydantic import BaseModel


class ModelRequest(BaseModel):
    capability: str
    input: dict[str, Any]
    output_schema_name: str


class ModelResult(BaseModel):
    output: dict[str, Any]
    provider: str
    model: str
    input_tokens: int = 0
    output_tokens: int = 0


class ModelGateway(Protocol):
    def invoke(self, request: ModelRequest) -> ModelResult: ...


class AgentRuntime(Protocol):
    def run(self, capability: str, input_data: dict[str, Any]) -> dict[str, Any]: ...


class UnitOfWork(Protocol):
    def __enter__(self) -> UnitOfWork: ...
    def __exit__(self, exc_type: object, exc: object, traceback: object) -> None: ...
    def commit(self) -> None: ...
    def rollback(self) -> None: ...
