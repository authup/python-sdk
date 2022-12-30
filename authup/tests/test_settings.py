import os
from unittest import mock

import pytest
from pydantic import ValidationError

from authup.authup import Settings


def test_settings_init():
    with pytest.raises(ValidationError):
        Settings()

    settings = Settings(
        url="https://authup.com",
        username="test",
        password="test",
    )

    with pytest.raises(ValidationError):
        Settings(
            url="https://authup.com",
            username="test",
        )

    with pytest.raises(ValidationError):
        Settings(
            url="https://authup.com",
            password="test",
            username=None,
        )

    with pytest.raises(ValidationError):
        Settings(
            url="https://authup.com",
            robot_id="test",
        )

    with pytest.raises(ValidationError):
        Settings(
            url="https://authup.com",
            robot_secret="test",
        )


def test_settings_from_env():

    with mock.patch.dict(os.environ, {"AUTHUP_URL": "https://authup.com"}):
        with pytest.raises(ValidationError):
            Settings()

    with mock.patch.dict(
        os.environ, {"AUTHUP_URL": "https://authup.com", "AUTHUP_USERNAME": "test"}
    ):
        with pytest.raises(ValidationError):
            Settings()

    with mock.patch.dict(
        os.environ,
        {
            "authup_url": "https://authup.com",
            "authup_password": "password",
            "authup_username": "username",
        },
    ):
        print(os.getenv("authup_url"))
        print(os.getenv("authup_password"))
        print(os.getenv("authup_username"))

        settings = Settings()
        assert settings.url == "https://authup.com"

    with mock.patch.dict(
        os.environ, {"AUTHUP_URL": "https://authup.com", "AUTHUP_ROBOT_ID": "test"}
    ):
        with pytest.raises(ValidationError):
            Settings()
    with mock.patch.dict(
        os.environ, {"AUTHUP_URL": "https://authup.com", "AUTHUP_ROBOT_SECRET": "test"}
    ):
        with pytest.raises(ValidationError):
            Settings()
    with mock.patch.dict(
        os.environ,
        {
            "AUTHUP_URL": "https://authup.com",
            "AUTHUP_ROBOT_ID": "test",
            "AUTHUP_ROBOT_SECRET": "test",
        },
    ):
        print("username", os.getenv("AUTHUP_USERNAME"))
        print("url", os.getenv("AUTHUP_URL"))

        Settings()
