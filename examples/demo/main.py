from contextlib import asynccontextmanager
from dataclasses import dataclass
from uuid import UUID
from typing import Annotated

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

from zmag.security import (
    CurrentUser,
    LoginForm,
    Token,
    User,
    authenticate_user,
    issue_access_token,
    set_refresh_cookie,
    validate_refresh_token,
)
from zmag.security.hashing import get_password_hash


@asynccontextmanager
async def lifespan(_: FastAPI):
    await DBLifespan.start()
    await create_tables(True)
    yield
    await DBLifespan.stop()


app = FastAPI(lifespan=lifespan)

for r in framework.components.api.values():
    app.include_router(r)


# ---------------------------------------------------------------------------
# Authentication
# ---------------------------------------------------------------------------


@app.post("/api/auth/login")
async def login(
    db: DatabaseSession,
    response: Response,
    form_data: OAuth2PasswordRequestForm = Depends(),
):
    user = await authenticate_user(db, form_data.username, form_data.password)

    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    response.set_cookie(
        key="access_token",
        value=issue_access_token(user),
        httponly=True,
        secure=True,
        samesite="strict",
    )
    set_refresh_cookie(response, user)
    return {"message": "logged in"}


@app.post("/api/auth/token")
async def login_for_access_token(
    db: DatabaseSession,
    response: Response,
    form_data: OAuth2PasswordRequestForm = Depends(),
):
    user = await authenticate_user(db, form_data.username, form_data.password)

    if not user:
        raise HTTPException(
            status_code=401,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    set_refresh_cookie(response, user)
    return Token(access_token=issue_access_token(user), token_type="bearer")


@app.post("/api/auth/token/refresh")
async def refresh_access_token(
    response: Response,
    user: Annotated[User, Depends(validate_refresh_token)],
) -> Token:
    set_refresh_cookie(response, user)  # token rotation
    return Token(access_token=issue_access_token(user), token_type="bearer")


@app.post("/api/auth/logout")
def logout(response: Response):
    response.delete_cookie("access_token")
    response.delete_cookie("refresh_token")
    return {"message": "logged out"}


@app.get("/api/auth/me")
async def read_users_me(current_user: CurrentUser) -> User:
    return current_user


@app.get("/api/auth/register")
async def create_user(db: DatabaseSession):
    User = get_model("auth", "User")
    user = User(email="john@doe.com", password=get_password_hash("secret"))
    await User.orm.create(db, user.__dict__)
    return


# ---------------------------------------------------------------------------
# APIs Handlers
# ---------------------------------------------------------------------------


@app.api_route(
    "/api/crud/{app_name}/{model_name}",
    methods=["GET", "POST", "PATCH", "DELETE"],
    tags=["crud"],
)
async def catch_all_public(
    request: Request,
    response: Response,
    db: DatabaseSession,
    current_user: CurrentUser,
    app_name: str,
    model_name: str,
):
    _app = app_name.replace("-", "_")
    _model = model_name.title().replace("-", "")
    db_model = get_model(_app, _model)
    crud_api = getattr(db_model, "CRUD", None)

    print(f"APP: {_app} | {_model}")
    if not db_model or not crud_api:
        raise HTTPException(status_code=404, detail="Not Found")

    meta, filters = parse_query(request.query_params)

    item_id = None
    if raw_id := meta.get("id"):
        try:
            item_id = UUID(raw_id)
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid ID format")

    body = {}
    if request.method in {"POST", "PATCH"}:
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
        user=current_user.model_dump(),
    )

    if request.method in {"DELETE", "PATCH"}:
        if not item_id:
            ctx.error(code="invalid", message="Must include an ID")

    try:
        match request.method:
            case "POST":
                result = await crud_api.create(db_model, ctx)
            case "PATCH":
                result = await crud_api.patch(db_model, ctx)
            case "DELETE":
                result = await crud_api.delete(db_model, ctx)
            case _:
                if item_id:
                    result = await crud_api.get(db_model, ctx)
                else:
                    result = await crud_api.list(db_model, ctx)
    except:  # noqa: E722
        result = None
        ctx.error(code="invalid", message="Invalid input")
    if len(ctx.errors):
        return {"data": None, "errors": ctx.errors}
    return {"data": result, "errors": []}
