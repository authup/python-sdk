import os

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from authup.plugins.asgi import AuthupASGIMiddleware
from authup.plugins.httpx import AuthupHttpx


@pytest.fixture
def fastapi_app():
    app = FastAPI()

    @app.get("/test")
    async def test():
        return {"message": "Hello World"}

    return app


@pytest.mark.asyncio
async def test_asgi_middleware(fastapi_app):

    fastapi_app.add_middleware(AuthupASGIMiddleware, authup_url="http://localhost:3010")

    auth = AuthupHttpx(
        url=os.getenv("AUTHUP_URL"),
        username=os.getenv("AUTHUP_USERNAME"),
        password=os.getenv("AUTHUP_PASSWORD"),
    )

    client = TestClient(fastapi_app)

    r = client.get("/test", auth=auth)
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
