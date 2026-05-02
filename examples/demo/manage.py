from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException
from fastapi import Request, Response
from fastapi.responses import HTMLResponse
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.staticfiles import StaticFiles


from zmag.framework.base import framework

from apps.sample_app.models import BlogPost, User

# Access registered components
# print(framework.components.models.get("sample.Blog"))
# data = BlogPost(tags=["1", "a"], meta={"1": "a"}, owner=User(), followers=[User()])
# print(data.id)
app = FastAPI()


@app.get("/api/public/{app_name}/{model_name}")
async def get_item_public(
    request: Request,
    app_name: str,
    model_name: str,
):

    return {
        "label": app_name,
        "model": model_name,
        "query": {},
        "filters": {},
        "user": None,
    }
