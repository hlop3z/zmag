from typing import Annotated
from fastapi import Depends

from .config import ACCESS_TOKEN_EXPIRE_MINUTES, REFRESH_TOKEN_EXPIRE_DAYS
from .dependencies import (
    authenticate_user,
    get_current_active_user,
    issue_access_token,
    set_refresh_cookie,
    validate_refresh_token,
)
from .schemas import LoginForm, Token, User
from .tokens import create_access_token, create_refresh_token

CurrentUser = Annotated[User, Depends(get_current_active_user)]

__all__ = (
    # Dependencies Quick Annotation
    "CurrentUser",
    # Config
    "ACCESS_TOKEN_EXPIRE_MINUTES",
    "REFRESH_TOKEN_EXPIRE_DAYS",
    # Dependencies & Logic
    "authenticate_user",
    "get_current_active_user",
    "issue_access_token",
    "set_refresh_cookie",
    "validate_refresh_token",
    # Schemas
    "LoginForm",
    "Token",
    "User",
    # Token Generation
    "create_access_token",
    "create_refresh_token",
)
