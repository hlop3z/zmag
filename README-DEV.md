# SQLAlchemy (recommended for most apps)

If you're using SQLAlchemy, lifespan usually controls the **engine**, not raw connections.

```python id="x8n2ld"
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from fastapi import FastAPI
from contextlib import asynccontextmanager

engine = None
SessionLocal = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    global engine, SessionLocal

    engine = create_async_engine("postgresql+asyncpg://user:pass@localhost/db")
    SessionLocal = async_sessionmaker(engine, expire_on_commit=False)

    yield

    await engine.dispose()

app = FastAPI(lifespan=lifespan)
```

---

# Common mistake (important)

A bad pattern:

```python
@app.get("/")
async def route():
    conn = await connect_db()  # ❌ new connection every request
```
