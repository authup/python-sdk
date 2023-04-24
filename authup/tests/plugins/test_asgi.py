import os

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from starlette.requests import Request

from authup.plugins.asgi import AuthupASGIMiddleware
from authup.plugins.httpx import AuthupHttpx


@pytest.fixture
def fastapi_app():
    app = FastAPI()

    @app.get("/test")
    async def test():
        return {"message": "Hello World"}

    @app.get("/test-user")
    async def test_user(request: Request):
        return {"message": "Hello World", "user": request.state.user}

    return app


@pytest.fixture
def httpx_auth():
    authup_url = os.getenv("AUTHUP_URL")
    username = os.getenv("AUTHUP_USERNAME")
    password = os.getenv("AUTHUP_PASSWORD")

    auth = AuthupHttpx(
        url=authup_url,
        username=username,
        password=password,
    )

    return auth


@pytest.mark.asyncio
async def test_asgi_middleware(fastapi_app, httpx_auth):

    fastapi_app.add_middleware(AuthupASGIMiddleware, authup_url="http://localhost:3010")

    client = TestClient(fastapi_app)

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
async def test_inject_user_middleware(fastapi_app, httpx_auth):
    fastapi_app.add_middleware(
        AuthupASGIMiddleware, authup_url="http://localhost:3010", user=True
    )

    client = TestClient(fastapi_app)

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
