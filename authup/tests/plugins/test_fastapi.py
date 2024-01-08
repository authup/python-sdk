import os

import pytest
from fastapi import Depends, FastAPI
from fastapi.testclient import TestClient

from authup.domains.schemas.token import Permission
from authup.domains.schemas.user import User
from authup.plugins.fastapi import AuthupUser
from authup.plugins.httpx import AuthupHttpx


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


# setup the fastapi app

app = FastAPI()

user_dependency = AuthupUser(url=os.getenv("AUTHUP_URL"))


@app.get("/test")
async def user_test(user: User = Depends(user_dependency)):
    return {"user": user.dict()}


permissions = [
    Permission(name="test", target="test", inverse=False, power=100000),
]

depends_unauthorized = AuthupUser(
    url=os.getenv("AUTHUP_URL"),
    permissions=permissions,
)

permissions_authorized = [
    Permission(name="client_add", inverse=False, power=100),
]

depends_authorized = AuthupUser(
    url=os.getenv("AUTHUP_URL"),
    permissions=permissions_authorized,
)


@app.get("/test-2")
async def user_test_2(user: User = Depends(depends_unauthorized)):
    return {"user": user.dict()}


@app.get("/test-authorized")
async def user_test_auth(user: User = Depends(depends_authorized)):
    return {"user": user.dict()}


client = TestClient(app)


def test_depends_user(httpx_auth):
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
    # insufficient permissions
    r = client.get("/test-2", auth=httpx_auth)
    print(r.content)
    assert r.status_code == 401

    # authorized
    r = client.get("/test-authorized", auth=httpx_auth)
    print(r.content)
    assert r.status_code == 200
    assert r.json()["user"]["name"] == "admin"
