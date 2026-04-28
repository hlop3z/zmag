from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException
from fastapi import Request, Response
from fastapi.responses import HTMLResponse
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.staticfiles import StaticFiles
from zmag.security import (
    Token,
    User,
    authenticate_user,
    fake_users_db,
    get_current_active_user,
    issue_access_token,
    set_refresh_cookie,
    validate_refresh_token,
)
from zmag.utils import load_template, parse_query
from zmag.middleware.sample import RejectBadTokenMiddleware

app = FastAPI()

app.add_middleware(RejectBadTokenMiddleware)

# ---------------------------------------------------------------------------
# Authentication
# ---------------------------------------------------------------------------


@app.post("/api/auth/login")
def login(response: Response, form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(fake_users_db, form_data.username, form_data.password)

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
def login_for_access_token(
    response: Response, form_data: OAuth2PasswordRequestForm = Depends()
):
    user = authenticate_user(fake_users_db, form_data.username, form_data.password)

    if not user:
        raise HTTPException(
            status_code=401,
            detail="Incorrect username or password",
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
async def read_users_me(
    current_user: Annotated[User, Depends(get_current_active_user)],
) -> User:
    return current_user


# ---------------------------------------------------------------------------
# APIs Handlers
# ---------------------------------------------------------------------------


@app.get("/api/public/{app_name}/{model_name}")
async def get_item_public(
    request: Request,
    app_name: str,
    model_name: str,
):
    query, filters = parse_query(request.query_params)
    return {
        "label": app_name,
        "model": model_name,
        "query": query,
        "filters": filters,
        "user": None,
    }


@app.get("/api/v1/{app_name}/{model_name}")
async def get_item(
    request: Request,
    current_user: Annotated[User, Depends(get_current_active_user)],
    app_name: str,
    model_name: str,
):
    query, filters = parse_query(request.query_params)
    return {
        "label": app_name,
        "model": model_name,
        "query": query,
        "filters": filters,
        "user": current_user.model_dump(),
    }


# ---------------------------------------------------------------------------
# Views
# ---------------------------------------------------------------------------

app.mount("/__static__", StaticFiles(directory="frontend/__static__"), name="static")
app.mount("/__assets__", StaticFiles(directory="frontend/__assets__"), name="assets")


@app.get("/{full_path:path}", response_class=HTMLResponse, tags=["views"])
async def root(request: Request, full_path: str):
    logged_in = "refresh_token" in request.cookies
    login_html = load_template("index.html")
    root_html = load_template("frontend/index.html")
    template = root_html if logged_in else login_html
    return template.render(full_path=full_path, logged_in=logged_in)
