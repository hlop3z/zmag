from contextlib import asynccontextmanager
from typing import AsyncGenerator, Annotated

from fastapi import FastAPI, Depends
from sqlalchemy.ext.asyncio import (
    create_async_engine,
    async_sessionmaker,
    AsyncSession,
)


from ..framework.sql_settings import DB_URL

# 1. Setup the Engine and Sessionmaker globally
engine = create_async_engine(DB_URL, echo=False)
async_session = async_sessionmaker(engine, expire_on_commit=False)


# 2. Lifespan instead of on_event
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup logic: No need to manually assign to app.state usually,
    # but you can if you need dynamic config.
    yield
    # Shutdown logic:
    await engine.dispose()


# 3. Dependency Injection
async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        yield session


# Define a type alias
DatabaseSession = Annotated[AsyncSession, Depends(get_db_session)]
