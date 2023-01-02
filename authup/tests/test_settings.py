import os
from unittest import mock

import pytest
from pydantic import ValidationError

from authup.authup import Settings


def test_settings_init():
    with pytest.raises(ValidationError):
        with mock.patch.dict(os.environ, {"AUTHUP_URL": "https://authup.org"}):
            Settings()

    settings = Settings(
        url="https://authup.org",
        username="test",
        password="test",
        robot_id=None,
        robot_secret=None,
    )
    assert settings.url == "https://authup.org"

    with pytest.raises(ValidationError):
        Settings(
            url="https://authup.org",
            username="test",
        )

    with pytest.raises(ValidationError):
        Settings(
            url="https://authup.org",
            password="test",
            username=None,
        )

    with pytest.raises(ValidationError):
        Settings(
            url="https://authup.org",
            robot_id="test",
        )

    with pytest.raises(ValidationError):
        Settings(
            url="https://authup.org",
            robot_secret="test",
        )


def test_settings_from_env():

    with mock.patch.dict(
        os.environ,
        {
            "AUTHUP_URL": "https://authup.org",
            "AUTHUP_USERNAME": "",
            "AUTHUP_PASSWORD": "",
            "AUTHUP_ROBOT_ID": "",
            "AUTHUP_ROBOT_SECRET": "",
        },
    ):
        with pytest.raises(ValidationError):
            Settings.from_env()

    with mock.patch.dict(
        os.environ, {"AUTHUP_URL": "https://authup.org", "AUTHUP_USERNAME": "test"}
    ):
        with pytest.raises(ValidationError):
            Settings.from_env()

    with mock.patch.dict(
        os.environ,
        {
            "authup_url": "https://authup.org",
            "authup_password": "password",
            "authup_username": "username",
            "AUTHUP_ROBOT_ID": "",
            "AUTHUP_ROBOT_SECRET": "",
        },
    ):
        print(os.getenv("authup_url"))
        print(os.getenv("authup_password"))
        print(os.getenv("authup_username"))

        settings = Settings.from_env()
        assert settings.url == "https://authup.org"

    with mock.patch.dict(
        os.environ, {"AUTHUP_URL": "https://authup.org", "AUTHUP_ROBOT_ID": "test"}
    ):
        with pytest.raises(ValidationError):
            Settings.from_env()
    with mock.patch.dict(
        os.environ, {"AUTHUP_URL": "https://authup.org", "AUTHUP_ROBOT_SECRET": "test"}
    ):
        with pytest.raises(ValidationError):
            Settings.from_env()
    with mock.patch.dict(
        os.environ,
        {
            "AUTHUP_URL": "https://authup.org",
            "authup_password": "",
            "authup_username": "",
            "AUTHUP_ROBOT_ID": "test",
            "AUTHUP_ROBOT_SECRET": "test",
        },
    ):
        print("username", os.getenv("AUTHUP_USERNAME"))
        print("url", os.getenv("AUTHUP_URL"))

        Settings.from_env()


def test_urls():

    settings = Settings(
        url="https://authup.org",
        username="test",
        password="test",
        robot_id=None,
        robot_secret=None,
    )
    assert settings.token_url == "https://authup.org/token"
    assert settings.user_url == "https://authup.org/users"
