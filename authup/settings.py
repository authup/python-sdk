import enum

from pydantic import BaseSettings, Field, root_validator, SecretStr


class CredentialTypes(enum.Enum):
    user = "user"
    robot = "robot"


def validate_check_credentials(
    username: str | None,
    password: str | None,
    robot_id: str | None,
    robot_secret: str | None,
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


class Settings(BaseSettings):
    url: str = Field(..., env="authup_url")
    username: str | None = Field(None, env="authup_username")
    password: SecretStr | None = Field(None, env="authup_password")
    robot_id: str | None = Field(None, env="authup_robot_id")
    robot_secret: SecretStr | None = Field(None, env="authup_robot_secret")

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
