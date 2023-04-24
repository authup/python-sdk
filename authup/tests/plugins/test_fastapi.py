import os

import pytest
from fastapi import Depends, FastAPI
from fastapi.testclient import TestClient

from authup.plugins.fastapi import AuthupUser
from authup.plugins.httpx import AuthupHttpx
from authup.schemas.token import Permission
from authup.schemas.user import User


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


def test_depends_user(httpx_auth):
    app = FastAPI()

    user_dependency = AuthupUser(url="http://localhost:3010")

    @app.get("/test")
    async def user_test(user: User = Depends(user_dependency)):
        return {"user": user.dict()}

    client = TestClient(app)

    authup_url = os.getenv("AUTHUP_URL")
    username = os.getenv("AUTHUP_USERNAME")
    password = os.getenv("AUTHUP_PASSWORD")

    auth = AuthupHttpx(
        url=authup_url,
        username=username,
        password=password,
    )

    r = client.get("/test", auth=auth)
    print(r.content)
    assert r.status_code == 200
    assert r.json()["user"]["name"] == "admin"

    # no token
    r = client.get("/test")
    assert r.status_code == 403

    r = client.get("/test", headers={"Authorization": "Bearer invalid"})
    assert r.status_code == 401


def test_depends_permissions(httpx_auth):
    app = FastAPI()

    permissions = [
        Permission(name="test", target="test", inverse=False, power=100000),
    ]

    depends_unauthorized = AuthupUser(
        url="http://localhost:3010",
        permissions=permissions,
    )

    permissions_authorized = [
        Permission(name="client_add", inverse=False, power=100),
    ]

    depends_authorized = AuthupUser(
        url="http://localhost:3010",
        permissions=permissions_authorized,
    )

    @app.get("/test")
    async def user_test(user: User = Depends(depends_unauthorized)):
        return {"user": user.dict()}

    @app.get("/test-authorized")
    async def user_test_auth(user: User = Depends(depends_authorized)):
        return {"user": user.dict()}

    client = TestClient(app)

    # insufficient permissions
    r = client.get("/test", auth=httpx_auth)
    print(r.content)
    assert r.status_code == 401

    # authorized
    r = client.get("/test-authorized", auth=httpx_auth)
    print(r.content)
    assert r.status_code == 200
    assert r.json()["user"]["name"] == "admin"
