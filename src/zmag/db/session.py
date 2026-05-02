"""
SQLAlchemy Session management.
"""

from typing import AsyncGenerator, Annotated

from fastapi import Depends

from sqlalchemy import MetaData
from sqlalchemy.pool import StaticPool
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from ..core.settings import settings
from .metadata import METADATA

engine: AsyncEngine = None  # type: ignore
SessionLocal = None

_SQLITE_KWARGS = dict(
    connect_args={"timeout": 30},
    poolclass=StaticPool,
)


class InternalError(Exception):
    pass


class DBLifespan:
    @staticmethod
    async def start():
        global engine, SessionLocal
        is_sqlite = settings.db_engine == "sqlite"
        engine = create_async_engine(
            settings.db_url,
            **(_SQLITE_KWARGS if is_sqlite else {}),
        )
        SessionLocal = async_sessionmaker(
            bind=engine, autoflush=False, expire_on_commit=False
        )

    @staticmethod
    async def stop():
        await engine.dispose()


async def create_tables(drop: bool = False):
    async with engine.begin() as conn:
        if drop:
            reflected = MetaData()
            await conn.run_sync(reflected.reflect)
            await conn.run_sync(reflected.drop_all)
        await conn.run_sync(METADATA.create_all)


async def db_session() -> AsyncGenerator[AsyncSession, None]:
    if not SessionLocal:
        raise RuntimeError("Database not initialised — lifespan did not run")
    async with SessionLocal() as session:
        try:
            yield session
            await session.commit()
        except:  # noqa: E722
            await session.rollback()
            raise InternalError("Database Error")
        finally:
            await session.close()


# Define a type alias
DatabaseSession = Annotated[AsyncSession, Depends(db_session)]
