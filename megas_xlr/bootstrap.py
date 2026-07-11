from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from megas_xlr.settings import Settings


def create_application(settings: Settings | None = None) -> FastAPI:
    resolved = settings or Settings()

    @asynccontextmanager
    async def lifespan(app: FastAPI) -> AsyncIterator[None]:
        app.state.settings = resolved
        yield

    app = FastAPI(title="Megas-xlr", lifespan=lifespan)

    @app.get("/health/live")
    async def liveness() -> dict[str, str]:
        return {"status": "alive"}

    @app.get("/health/ready")
    async def readiness() -> dict[str, str]:
        return {"status": "ready"}

    return app
