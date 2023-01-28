import enum
import os
from typing import Optional

from pydantic import BaseModel, SecretStr, root_validator


class CredentialTypes(enum.Enum):
    user = "user"
    robot = "robot"


class EnvVars(enum.Enum):
    url = "URL"
    username = "USERNAME"
    password = "PASSWORD"
    robot_id = "ROBOT_ID"
    robot_secret = "ROBOT_SECRET"


def validate_check_credentials(
    username: str = None,
    password: str = None,
    robot_id: str = None,
    robot_secret: str = None,
) -> CredentialTypes:
    if not username and not robot_id:
        raise ValueError("No username or robot_id provided")

    if robot_secret and password:
        raise ValueError("Both password and robot_secret provided")

    if username and robot_id:
        raise ValueError("Only username or robot_id can be provided")

    if username and not password:
        raise ValueError("No password provided for username")

    if robot_id and not robot_secret:
        raise ValueError("No robot_secret provided for robot_id")

    if username:
        return CredentialTypes.user
    else:
        return CredentialTypes.robot


class Settings(BaseModel):
    url: str
    username: Optional[str] = None
    password: Optional[SecretStr] = None
    robot_id: Optional[str] = None
    robot_secret: Optional[SecretStr] = None

    @property
    def token_url(self):
        return f"{self.url}/token"

    @property
    def user_url(self):
        return f"{self.url}/users"

    @root_validator
    def validate_settings(cls, values):
        validate_check_credentials(
            values.get("username"),
            values.get("password"),
            values.get("robot_id"),
            values.get("robot_secret"),
        )
        return values

    @classmethod
    def from_env(cls, prefix: str = "AUTHUP") -> "Settings":
        settings_dict = {}
        for env_var in EnvVars:
            settings_dict[env_var.name] = os.getenv(f"{prefix}_{env_var.value}")
        return cls(**settings_dict)
