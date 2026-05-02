from contextlib import asynccontextmanager
from dataclasses import dataclass
from uuid import UUID
from typing import Any

from fastapi import Depends, FastAPI, HTTPException
from fastapi import Request, Response
from fastapi.responses import HTMLResponse
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.staticfiles import StaticFiles


from zmag.framework.base import framework
from zmag.framework.apps import get_model
from zmag.utils import parse_query, Pagination
from zmag.core.context import Context
from zmag.db.session import DBLifespan, create_tables, DatabaseSession

from apps.sample_app.models import Blog
from apps.auth.models import User


@asynccontextmanager
async def lifespan(_: FastAPI):
    await DBLifespan.start()
    await create_tables(True)
    yield
    await DBLifespan.stop()


app = FastAPI(lifespan=lifespan)

for r in framework.components.api.values():
    app.include_router(r)


@app.api_route(
    "/api/public/{app_name}/{model_name}",
    methods=["GET", "POST", "PUT", "PATCH", "DELETE"],
)
async def catch_all_public(
    request: Request,
    response: Response,
    db: DatabaseSession,
    app_name: str,
    model_name: str,
):
    _app = app_name.replace("-", "_")
    _model = model_name.title().replace("-", "")
    db_model = get_model(_app, _model)
    crud_api = getattr(db_model, "CRUD", None)

    if not db_model or not crud_api:
        raise HTTPException(status_code=404, detail="Not Found")

    meta, filters = parse_query(request.query_params)

    item_id = None
    if raw_id := meta.get("id"):
        try:
            item_id = UUID(raw_id)
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid id format")

    body = {}
    if request.method in {"POST", "PUT", "PATCH"}:
        try:
            body = await request.json()
        except Exception:
            pass

    ctx = Context.init(
        db=db,
        id=item_id,
        input=body,
        pagination=meta,
        filters=filters,
        request=request,
        response=response,
    )

    match request.method:
        case "POST":
            result = await crud_api.create(db_model, ctx)
        case "PUT":
            result = await crud_api.update(db_model, ctx)
        case "PATCH":
            result = await crud_api.patch(db_model, ctx)
        case "DELETE":
            result = await crud_api.delete(db_model, ctx)
        case _:
            if item_id:
                result = await crud_api.get(db_model, ctx)
            else:
                result = await crud_api.list(db_model, ctx)

    return {"data": result}
