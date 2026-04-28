# Limiter

---

## ✅ 1. Use `user_id` as the rate limit key

Instead of:

```python
key_func=get_remote_address
```

You define your own:

```python id="sl1"
def get_user_id(request):
    return str(request.state.user_id)
```

Then:

```python id="sl2"
limiter = Limiter(
    key_func=get_user_id,
    storage_uri="redis://localhost:6379"
)
```

---

## ✅ 2. Example with authentication (FastAPI)

You need to extract `user_id` earlier (middleware or dependency):

```python id="sl3"
from fastapi import FastAPI, Request

app = FastAPI()

@app.middleware("http")
async def add_user_to_request(request: Request, call_next):
    # Example: pull from header / JWT / session
    request.state.user_id = request.headers.get("X-User-ID", "anonymous")
    return await call_next(request)
```

Now rate limiting uses that:

```python id="sl4"
@limiter.limit("10/minute")
@app.get("/")
async def home(request: Request):
    return {"ok": True}
```

---

## ✅ 3. Combine user_id + IP (recommended)

Using only `user_id` has a weakness:

- users can share accounts
- attackers can spoof IDs if auth is weak

Better approach:

```python id="sl5"
def user_or_ip(request):
    user_id = getattr(request.state, "user_id", None)
    ip = request.client.host

    if user_id:
        return f"user:{user_id}"
    return f"ip:{ip}"
```

---

## ✅ 4. Advanced: strict composite key

If you want BOTH enforced:

```python id="sl6"
def user_and_ip(request):
    user_id = getattr(request.state, "user_id", "anon")
    ip = request.client.host
    return f"{user_id}:{ip}"
```
