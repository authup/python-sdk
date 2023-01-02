import os

import pytest

from authup import get_token, get_token_async
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())


def test_get_token():
    authup_url = os.getenv("AUTHUP_URL")
    print(authup_url)
    token_url = authup_url + "/token"

    with pytest.raises(ValueError):
        get_token(token_url=None)

    # test with username and password
    username = os.getenv("AUTHUP_USERNAME")
    password = os.getenv("AUTHUP_PASSWORD")

    print(username, password)

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

    robot_id = os.getenv("AUTHUP_ROBOT_ID")
    robot_secret = os.getenv("AUTHUP_ROBOT_SECRET")

    print(robot_id, robot_secret)

    token = get_token(token_url=token_url, robot_id=robot_id, robot_secret=robot_secret)

    assert token.access_token
    assert token.token_type == "Bearer"
    assert token.expires_in > 0
    assert not token.refresh_token

    # check errors for incorrect username and password / robot_id and robot_secret

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
async def test_get_token_async():
    authup_url = os.getenv("AUTHUP_URL")
    print(authup_url)
    token_url = authup_url + "/token"

    with pytest.raises(ValueError):
        await get_token_async(token_url=None)

    # test with username and password
    username = os.getenv("AUTHUP_USERNAME")
    password = os.getenv("AUTHUP_PASSWORD")

    print(username, password)

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

    robot_id = os.getenv("AUTHUP_ROBOT_ID")
    robot_secret = os.getenv("AUTHUP_ROBOT_SECRET")

    print(robot_id, robot_secret)

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
