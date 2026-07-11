from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session, sessionmaker

from megas_xlr.settings import DatabaseSettings


def create_engine_factory(settings: DatabaseSettings) -> Engine:
    return create_engine(settings.url, pool_pre_ping=True, pool_size=settings.pool_size)


def create_session_factory(engine: Engine) -> sessionmaker[Session]:
    return sessionmaker(bind=engine, expire_on_commit=False)


class SqlAlchemyUnitOfWork:
    def __init__(self, factory: sessionmaker[Session]) -> None:
        self._factory = factory
        self.session: Session | None = None

    def __enter__(self) -> SqlAlchemyUnitOfWork:
        self.session = self._factory()
        self.session.begin()
        return self

    def __exit__(self, exc_type: object, exc: object, traceback: object) -> None:
        if self.session is None:
            return
        if exc is None:
            self.session.commit()
        else:
            self.session.rollback()
        self.session.close()

    def commit(self) -> None:
        if self.session is None:
            raise RuntimeError("unit of work is not active")
        self.session.commit()

    def rollback(self) -> None:
        if self.session is None:
            raise RuntimeError("unit of work is not active")
        self.session.rollback()
