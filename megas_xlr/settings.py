from enum import StrEnum
from pathlib import Path

from pydantic import BaseModel, Field, SecretStr, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Environment(StrEnum):
    DEVELOPMENT = "development"
    TEST = "test"
    PRODUCTION = "production"


class DatabaseSettings(BaseModel):
    url: str = "postgresql+psycopg://megas:megas_local_dev@localhost:5433/megas_xlr"
    agno_schema: str = "agno"
    pool_size: int = Field(default=5, ge=1)


class AuthSettings(BaseModel):
    issuer: str = "megas-xlr"
    audience: str = "megas-xlr-adapter"
    token_ttl_seconds: int = Field(default=900, ge=60, le=3600)
    signing_key: SecretStr | None = None
    github_client_id: str | None = None
    github_client_secret: SecretStr | None = None
    github_redirect_uri: str = "http://127.0.0.1:7777/v1/auth/github/callback"


class StorageSettings(BaseModel):
    backend: str = "local"
    local_path: Path = Path(".data/artifacts")
    evidence_ttl_hours: int = Field(default=24, ge=1)


class ProviderSettings(BaseModel):
    enabled: bool = False
    approved_models: tuple[str, ...] = ()


class BudgetSettings(BaseModel):
    simple_soft_usd: float = 0.5
    medium_soft_usd: float = 3.0
    critical_soft_usd: float = 15.0
    hard_multiplier: float = Field(default=2.0, ge=1.0)


class TelemetrySettings(BaseModel):
    enabled: bool = False
    service_name: str = "megas-xlr"
    otlp_endpoint: str | None = None
    include_source: bool = False


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix="MEGAS_",
        env_nested_delimiter="__",
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    environment: Environment = Environment.DEVELOPMENT
    db: DatabaseSettings = Field(default_factory=DatabaseSettings)
    auth: AuthSettings = Field(default_factory=AuthSettings)
    storage: StorageSettings = Field(default_factory=StorageSettings)
    providers: ProviderSettings = Field(default_factory=ProviderSettings)
    budgets: BudgetSettings = Field(default_factory=BudgetSettings)
    telemetry: TelemetrySettings = Field(default_factory=TelemetrySettings)
    disabled_capabilities: frozenset[str] = frozenset()

    @model_validator(mode="after")
    def validate_production_secrets(self) -> Settings:
        if self.environment is Environment.PRODUCTION:
            required = (
                self.auth.signing_key,
                self.auth.github_client_id,
                self.auth.github_client_secret,
            )
            if any(value is None for value in required):
                raise ValueError("production requires signing and GitHub OAuth credentials")
        return self
