from zmag import include_router

from fastapi import APIRouter

api = APIRouter(prefix="/users", tags=["users"])
include_router(api)


@api.get("/")
async def read_users():
    return [{"username": "Rick"}, {"username": "Morty"}]
