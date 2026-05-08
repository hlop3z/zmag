from datetime import timedelta
from typing import Annotated

import jwt
from fastapi import Depends, HTTPException, Request, Response, status
from fastapi.security import OAuth2PasswordBearer
from jwt.exceptions import InvalidTokenError

from ..db.session import DatabaseSession
from ..framework.apps import get_model
from .config import (
    ACCESS_TOKEN_EXPIRE_MINUTES,
    ALGORITHM,
    REFRESH_TOKEN_EXPIRE_DAYS,
    SECRET_KEY,
    TOKEN_URL,
)
from .hashing import DUMMY_HASH, verify_password
from .schemas import TokenData, User
from .tokens import create_access_token, create_refresh_token

_REFRESH_MAX_AGE = timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=TOKEN_URL.lstrip("/"), auto_error=False)


async def get_token(
    request: Request,
    token: Annotated[str | None, Depends(oauth2_scheme)] = None,
) -> str:
    if token:
        return token

    cookie_token = request.cookies.get("access_token")
    if cookie_token:
        return cookie_token

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Not authenticated",
        headers={"WWW-Authenticate": "Bearer"},
    )


async def _get_user(db, email: str) -> User | None:
    UserModel = get_model("auth", "User")
    if UserModel is None:
        return None
    row = await UserModel.orm.get_by(db, email=email)
    if row is None:
        return None
    return User(
        id=row["id"],
        email=row["email"],
        full_name=row.get("full_name"),
        disabled=row.get("disabled", False),
    )


async def authenticate_user(db, email: str, password: str) -> User | None:
    UserModel = get_model("auth", "User")
    if UserModel is None:
        verify_password(password, DUMMY_HASH)
        return None
    row = await UserModel.orm.get_by(db, email=email)
    if not row:
        verify_password(password, DUMMY_HASH)
        return None
    if not verify_password(password, row["password"]):
        return None
    return User(
        id=row["id"],
        email=row["email"],
        full_name=row.get("full_name"),
        disabled=row.get("disabled", False),
    )


async def get_current_user(
    db: DatabaseSession,
    token: Annotated[str, Depends(get_token)],
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("sub")
        if email is None:
            raise credentials_exception
        token_data = TokenData(email=email)
    except InvalidTokenError:
        raise credentials_exception
    user = await _get_user(db, token_data.email)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user)],
):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Not authenticated")
    return current_user


def issue_access_token(user: User) -> str:
    return create_access_token(
        data={"sub": user.email},
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
    )


def set_refresh_cookie(response: Response, user: User) -> None:
    token = create_refresh_token(data={"sub": user.email})
    response.set_cookie(
        key="refresh_token",
        value=token,
        httponly=True,
        secure=True,
        samesite="strict",
        max_age=int(_REFRESH_MAX_AGE.total_seconds()),
    )


async def validate_refresh_token(db: DatabaseSession, request: Request) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid refresh token",
    )
    token = request.cookies.get("refresh_token")
    if not token:
        raise credentials_exception
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        if payload.get("type") != "refresh":
            raise credentials_exception
        email: str | None = payload.get("sub")
        if email is None:
            raise credentials_exception
    except InvalidTokenError:
        raise credentials_exception
    user = await _get_user(db, email)
    if user is None or user.disabled:
        raise credentials_exception
    return user
