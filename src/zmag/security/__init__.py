from typing import Annotated
from fastapi import Depends

from .config import (
    ACCESS_TOKEN_EXPIRE_MINUTES,
    REFRESH_TOKEN_EXPIRE_DAYS,
    fake_users_db,
)
from .dependencies import (
    authenticate_user,
    get_current_active_user,
    issue_access_token,
    set_refresh_cookie,
    validate_refresh_token,
)
from .schemas import Token, User
from .tokens import create_access_token, create_refresh_token

CurrentUser = Annotated[User, Depends(get_current_active_user)]

__all__ = (
    # Dependencies Quick Annotation
    "CurrentUser",
    # Config & Data
    "ACCESS_TOKEN_EXPIRE_MINUTES",
    "REFRESH_TOKEN_EXPIRE_DAYS",
    "fake_users_db",
    # Dependencies & Logic
    "authenticate_user",
    "get_current_active_user",
    "issue_access_token",
    "set_refresh_cookie",
    "validate_refresh_token",
    # Schemas
    "Token",
    "User",
    # Token Generation
    "create_access_token",
    "create_refresh_token",
)
