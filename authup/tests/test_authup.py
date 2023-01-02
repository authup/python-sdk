import os

import pytest

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
