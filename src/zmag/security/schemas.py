from pydantic import BaseModel
from uuid import UUID


class LoginForm(BaseModel):
    email: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: str | None = None


class User(BaseModel):
    id: UUID
    email: str
    full_name: str | None = None
    disabled: bool | None = None


class UserInDB(User):
    hashed_password: str
