import os

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from starlette.requests import Request

from ...plugins.asgi import AuthupASGIMiddleware


def fastapi_app():
    app = FastAPI()

    @app.get("/test")
    async def test():
        print("test route called")
        return {"message": "Hello World"}

    @app.get("/test-user")
    async def test_user(request: Request):
        return {"message": "Hello World", "user": request.state.user}

    return app


@pytest.mark.asyncio
async def test_asgi_middleware(httpx_auth):
    app = fastapi_app()
    client = TestClient(app)

    app.add_middleware(AuthupASGIMiddleware, authup_url=os.getenv("AUTHUP_URL"))

    r = client.get("/test", auth=httpx_auth)
    print(r.content)

    assert r.status_code == 200
    assert r.json() == {"message": "Hello World"}

    # invalid token
    r = client.get("/test", headers={"Authorization": "Bearer invalid"})
    assert r.status_code == 401

    # no header
    r = client.get("/test")
    assert r.status_code == 401

    # invalid header invalid key
    r = client.get("/test", headers={"Authorizatio": "Bearer invalid"})
    assert r.status_code == 401

    # invalid header no two parts
    r = client.get("/test", headers={"Authorization": "invalid"})
    assert r.status_code == 401

    # invalid header bearer wrong
    r = client.get("/test", headers={"Authorization": "Beare invalid"})
    assert r.status_code == 401


@pytest.mark.asyncio
async def test_inject_user_middleware(httpx_auth):
    app = fastapi_app()
    client = TestClient(app)

    app.add_middleware(
        AuthupASGIMiddleware, authup_url=os.getenv("AUTHUP_URL"), user=True
    )

    r = client.get("/test-user", auth=httpx_auth)
    print(r.content)
    assert r.status_code == 200
    assert r.json()["user"]["name"] == "admin"

    # invalid token
    r = client.get("/test-user", headers={"Authorization": "Bearer invalid"})
    assert r.status_code == 401

    # no header
    r = client.get("/test-user")
    assert r.status_code == 401

    # invalid header invalid key
    r = client.get("/test-user", headers={"Authorizatio": "Bearer invalid"})
    assert r.status_code == 401

    # invalid header no two parts
    r = client.get("/test-user", headers={"Authorization": "invalid"})
    assert r.status_code == 401

    # invalid header bearer wrong
    r = client.get("/test-user", headers={"Authorization": "Beare invalid"})
    assert r.status_code == 401
