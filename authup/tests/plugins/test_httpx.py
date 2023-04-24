import os

import httpx
import pytest

from authup.plugins.httpx import AuthupHttpx


@pytest.fixture
def auth_credentials():
    authup_url = os.getenv("AUTHUP_URL")
    username = os.getenv("AUTHUP_USERNAME")
    password = os.getenv("AUTHUP_PASSWORD")
    return authup_url, username, password


def test_auth_flow(auth_credentials):
    authup_url, username, password = auth_credentials
    auth = AuthupHttpx(
        url=authup_url,
        username=username,
        password=password,
    )

    r = httpx.get(authup_url + "/users/@me", auth=auth)
    assert r.status_code == 200


@pytest.mark.asyncio
async def test_auth_flow_async(auth_credentials):
    authup_url, username, password = auth_credentials
    auth = AuthupHttpx(
        url=authup_url,
        username=username,
        password=password,
    )

    # test with async and with client instance
    async with httpx.AsyncClient(auth=auth) as client:
        r = await client.get(authup_url + "/users/@me")
        assert r.status_code == 200
