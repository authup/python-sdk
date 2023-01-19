import asyncio
import os
import platform

import httpx
import pytest

from authup import Authup
from authup.client import AuthupClient
from authup.plugins.httpx import AuthupHttpx


@pytest.fixture(scope="session")
def event_loop():
    if platform.system() == "Windows":
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
    yield loop
    loop.close()


def pytest_sessionfinish(session, exitstatus):
    asyncio.get_event_loop().close()


@pytest.fixture(scope="session", autouse=True)
def authup_instance():
    authup = Authup(
        url=os.getenv("AUTHUP_URL"),
        username=os.getenv("AUTHUP_USERNAME"),
        password=os.getenv("AUTHUP_PASSWORD"),
    )
    return authup


@pytest.fixture(scope="session", autouse=True)
def robot_creds(authup_instance):
    secret = os.getenv("AUTHUP_ROBOT_SECRET")

    auth = AuthupHttpx(
        url=authup_instance.settings.url,
        username=authup_instance.settings.username,
        password=authup_instance.settings.password.get_secret_value(),
    )

    r = httpx.get(authup_instance.settings.url + "/robots", auth=auth)

    robot_id = r.json()["data"][0]["id"]

    return robot_id, secret


@pytest.fixture(scope="session", autouse=True)
def authup_client(authup_instance):
    client = AuthupClient(
        authup_url=authup_instance.settings.url,
        username=authup_instance.settings.username,
        password=authup_instance.settings.password.get_secret_value(),
    )
    return client
