import datetime
import os

import pytest
from dotenv import find_dotenv, load_dotenv

from authup import Authup
from authup.settings import Settings


def test_init():
    authup = Authup(
        url="https://authup.org",
        username="test",
        password="test",
        robot_id=None,
        robot_secret=None,
    )
    assert authup.settings.url == "https://authup.org"
    assert authup.settings.username == "test"
    print(authup)

    username = os.getenv("AUTHUP_USERNAME")
    password = os.getenv("AUTHUP_PASSWORD")
    robot_id = os.getenv("AUTHUP_ROBOT_ID")
    robot_secret = os.getenv("AUTHUP_ROBOT_SECRET")

    # test with username and password
    authup = Authup(url="https://authup.org", username=username, password=password)

    assert authup.settings.url == "https://authup.org"
    assert authup.settings.username == username
    assert authup.settings.password.get_secret_value() == password

    # test with robot_id and robot_secret via settings object
    test_settings = Settings(
        url="https://authup.org",
        robot_id=robot_id,
        robot_secret=robot_secret,
        username=None,
        password=None,
    )

    authup = Authup(settings=test_settings)
    assert authup.settings.url == "https://authup.org"
    assert authup.settings.robot_id == robot_id
    assert authup.settings.robot_secret.get_secret_value() == robot_secret
    print(authup)

    # no url
    with pytest.raises(ValueError):
        Authup(
            url=None,
            username=username,
            password=password,
        )


@pytest.mark.asyncio
async def test_get_token():
    load_dotenv(find_dotenv())
    authup_url = os.getenv("AUTHUP_URL")
    print(authup_url)

    # test with username and password
    username = os.getenv("AUTHUP_USERNAME")
    password = os.getenv("AUTHUP_PASSWORD")
    robot_id = os.getenv("AUTHUP_ROBOT_ID")
    robot_secret = os.getenv("AUTHUP_ROBOT_SECRET")

    # test sync + async with username and password

    authup = Authup(url=authup_url, username=username, password=password)

    token = authup.get_token()

    assert token
    assert token.access_token
    assert token.refresh_token

    token = await authup.get_token_async()
    assert token
    assert token.access_token

    # test sync + async with robot_id and robot_secret
    print(robot_id, robot_secret)

    authup = Authup(url=authup_url, robot_id=robot_id, robot_secret=robot_secret)

    token = authup.get_token()
    assert token
    assert token.access_token
    assert not token.refresh_token

    token = await authup.get_token_async()
    assert token
    assert token.access_token


def test_headers():
    authup = Authup(
        url=os.getenv("AUTHUP_URL"),
        username=os.getenv("AUTHUP_USERNAME"),
        password=os.getenv("AUTHUP_PASSWORD"),
    )

    headers = authup.authorization_header
    assert headers

    authup.token_expires_at = datetime.datetime.now() - datetime.timedelta(seconds=1)
    headers = authup.authorization_header

    assert headers
    assert authup.token_expires_at > datetime.datetime.now()

