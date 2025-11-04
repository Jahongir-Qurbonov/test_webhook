from asyncio import current_task
from contextlib import asynccontextmanager
from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_scoped_session,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import DeclarativeBase, declarative_base

from .config import settings

# Base model
Base: type[DeclarativeBase] = declarative_base()

# Cache scoped session
__async_session_factory: async_scoped_session[AsyncSession] | None = None


def get_session_factory() -> async_scoped_session[AsyncSession]:
    global __async_session_factory

    if __async_session_factory is None:
        engine = create_async_engine(
            str(settings.SQLALCHEMY_DATABASE_SQLITE_URI),
            echo=False,
        )

        __async_session_factory = async_scoped_session(
            async_sessionmaker(
                bind=engine,
                autocommit=False,
                autoflush=False,
            ),
            scopefunc=current_task,
        )

    return __async_session_factory


async def session() -> AsyncGenerator[AsyncSession]:
    _session_factory = get_session_factory()
    _session = _session_factory()

    try:
        yield _session
    except Exception:
        await _session.rollback()
        raise
    finally:
        await _session.close()


session_context = asynccontextmanager(session)


async def init_db() -> None:
    async with session_context() as _session:
        await _session.run_sync(lambda s: Base.metadata.create_all(bind=s.get_bind()))
