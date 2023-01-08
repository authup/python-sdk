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
            "AUTHUP_URL": "https://authup.org",
            "AUTHUP_PASSWORD": "password",
            "AUTHUP_USERNAME": "username",
            "AUTHUP_ROBOT_ID": "",
            "AUTHUP_ROBOT_SECRET": "",
        },
    ):

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
            "AUTHUP_PASSWORD": "",
            "AUTHUP_USERNAME": "",
            "AUTHUP_ROBOT_ID": "test",
            "AUTHUP_ROBOT_SECRET": "test",
        },
    ):

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
