import os

import pytest
from dotenv import find_dotenv, load_dotenv

from authup import get_token, get_token_async
from authup.token import (
    introspect_token,
    introspect_token_async,
    refresh_token,
    refresh_token_async,
)

load_dotenv(find_dotenv())


# @pytest.fixture
# def authup_instance():
#     authup = Authup(
#         url=os.getenv("AUTHUP_URL"),
#         username=os.getenv("AUTHUP_USERNAME"),
#         password=os.getenv("AUTHUP_PASSWORD"),
#     )
#     return authup
#
#
# @pytest.fixture
# def robot_creds(authup_instance):
#     secret = os.getenv("AUTHUP_ROBOT_SECRET")
#
#     auth = AuthupHttpx(
#         url=authup_instance.settings.url,
#         username=authup_instance.settings.username,
#         password=authup_instance.settings.password.get_secret_value(),
#     )
#
#     r = httpx.get(authup_instance.settings.url + "/robots", auth=auth)
#
#     robot_id = r.json()["data"][0]["id"]
#
#     return robot_id, secret


def test_get_token(robot_creds):
    authup_url = os.getenv("AUTHUP_URL")
    token_url = authup_url + "/token"

    with pytest.raises(ValueError):
        get_token(token_url=None)

    # test with username and password
    username = os.getenv("AUTHUP_USERNAME")
    password = os.getenv("AUTHUP_PASSWORD")

    token = get_token(
        token_url=token_url,
        username=username,
        password=password,
    )

    assert token.access_token
    assert token.token_type == "Bearer"
    assert token.expires_in > 0
    assert token.refresh_token

    # test with robot_id and robot_secret
    robot_id, robot_secret = robot_creds

    assert robot_id
    assert robot_secret

    token = get_token(token_url=token_url, robot_id=robot_id, robot_secret=robot_secret)

    assert token.access_token
    assert token.token_type == "Bearer"
    assert token.expires_in > 0
    assert not token.refresh_token

    # check errors for incorrect username and password / robot_id and robot_secret

    with pytest.raises(ValueError):
        get_token(
            token_url=None,
            username=username,
            password=None,
        )

    # username + robot_id
    with pytest.raises(ValueError):
        get_token(
            token_url=token_url,
            username=username,
            password=password,
            robot_id=robot_id,
        )

    # username + no password
    with pytest.raises(ValueError):
        get_token(
            token_url=token_url,
            username=username,
            password=None,
        )

    # password + no username
    with pytest.raises(ValueError):
        get_token(
            token_url=token_url,
            username=None,
            password=password,
        )

    # robot_id + no robot_secret
    with pytest.raises(ValueError):
        get_token(
            token_url=token_url,
            robot_id=robot_id,
            robot_secret=None,
        )

    # robot_secret + no robot_id
    with pytest.raises(ValueError):
        get_token(
            token_url=token_url,
            robot_id=None,
            robot_secret=robot_secret,
        )

    # no username, password, robot_id, robot_secret
    with pytest.raises(ValueError):
        get_token(
            token_url=token_url,
            username=None,
            password=None,
            robot_id=None,
            robot_secret=None,
        )


@pytest.mark.asyncio
async def test_get_token_async(robot_creds):
    authup_url = os.getenv("AUTHUP_URL")
    token_url = authup_url + "/token"

    with pytest.raises(ValueError):
        await get_token_async(token_url=None)

    # test with username and password
    username = os.getenv("AUTHUP_USERNAME")
    password = os.getenv("AUTHUP_PASSWORD")

    token = await get_token_async(
        token_url=token_url,
        username=username,
        password=password,
    )

    assert token.access_token
    assert token.token_type == "Bearer"
    assert token.expires_in > 0
    assert token.refresh_token

    # test with robot_id and robot_secret

    robot_id, robot_secret = robot_creds

    token = await get_token_async(
        token_url=token_url, robot_id=robot_id, robot_secret=robot_secret
    )

    assert token.access_token
    assert token.token_type == "Bearer"
    assert token.expires_in > 0
    assert not token.refresh_token

    # check errors for incorrect username and password / robot_id and robot_secret

    # username + robot_id
    with pytest.raises(ValueError):
        await get_token_async(
            token_url=token_url,
            username=username,
            password=password,
            robot_id=robot_id,
        )

    # username + no password
    with pytest.raises(ValueError):
        await get_token_async(
            token_url=token_url,
            username=username,
            password=None,
        )

    # password + no username
    with pytest.raises(ValueError):
        await get_token_async(
            token_url=token_url,
            username=None,
            password=password,
        )

    # robot_id + no robot_secret
    with pytest.raises(ValueError):
        await get_token_async(
            token_url=token_url,
            robot_id=robot_id,
            robot_secret=None,
        )

    # robot_secret + no robot_id
    with pytest.raises(ValueError):
        await get_token_async(
            token_url=token_url,
            robot_id=None,
            robot_secret=robot_secret,
        )

    # no username, password, robot_id, robot_secret
    with pytest.raises(ValueError):
        await get_token_async(
            token_url=token_url,
            username=None,
            password=None,
            robot_id=None,
            robot_secret=None,
        )


@pytest.mark.asyncio
async def test_introspect_token_async():
    authup_url = os.getenv("AUTHUP_URL")
    token_url = authup_url + "/token"
    introspect_url = token_url + "/introspect"

    # test with username and password
    username = os.getenv("AUTHUP_USERNAME")
    password = os.getenv("AUTHUP_PASSWORD")

    token = await get_token_async(
        token_url=token_url,
        username=username,
        password=password,
    )

    assert token.access_token

    introspect_result = await introspect_token_async(
        token_introspect_url=introspect_url,
        token=token.access_token,
    )

    assert introspect_result

    with pytest.raises(Exception):
        await introspect_token_async(
            token_introspect_url=introspect_url,
            token="token.access_token",
        )

    with pytest.raises(ValueError):
        await introspect_token_async(
            token_introspect_url=None,
            token="token.access_token",
        )

    with pytest.raises(ValueError):
        await introspect_token_async(
            token_introspect_url=introspect_url,
            token=None,
        )


def test_introspect_token():
    authup_url = os.getenv("AUTHUP_URL")
    token_url = authup_url + "/token"
    introspect_url = token_url + "/introspect"

    # test with username and password
    username = os.getenv("AUTHUP_USERNAME")
    password = os.getenv("AUTHUP_PASSWORD")

    token = get_token(
        token_url=token_url,
        username=username,
        password=password,
    )

    assert token.access_token

    introspect_result = introspect_token(
        token_introspect_url=introspect_url,
        token=token.access_token,
    )

    assert introspect_result

    with pytest.raises(Exception):
        introspect_token(
            token_introspect_url=introspect_url,
            token="token.access_token",
        )

    with pytest.raises(ValueError):
        introspect_token(token_introspect_url=introspect_url, token=None)

    with pytest.raises(ValueError):
        introspect_token(token_introspect_url=None, token="test")


@pytest.mark.asyncio
async def test_refresh_token_async(authup_instance):
    token = await authup_instance.get_token_async()

    assert token.access_token

    refreshed_token = await refresh_token_async(
        authup_instance.settings.token_url, token.refresh_token
    )

    assert refreshed_token.access_token

    assert refreshed_token.access_token != token.access_token


def test_refresh_token(authup_instance):
    authup_instance.token = None
    token = authup_instance.get_token()

    assert token.access_token

    refreshed_token = refresh_token(
        authup_instance.settings.token_url, token.refresh_token
    )

    assert refreshed_token.access_token

    assert refreshed_token.access_token != token.access_token
