from pydantic import BaseSettings, Field, root_validator


class Settings(BaseSettings):
    url: str = Field(..., env="authup_url")
    username: str = Field(None, env="authup_username")
    password: str = Field(None, env="authup_password")
    robot_id: str = Field(None, env="authup_robot_id")
    robot_secret: str = Field(None, env="authup_robot_secret")

    @property
    def token_url(self):
        return f"{self.url}/token"

    @property
    def user_url(self):
        return f"{self.url}/users"

    @root_validator
    def validate_settings(cls, values):
        if values.get("username") and not values.get("password"):
            raise ValueError("Password is required when username is provided")

        if values.get("password") and not values.get("username"):
            raise ValueError("Username is required when password is provided")

        if values.get("robot_id") and not values.get("robot_secret"):
            raise ValueError("Robot secret is required when robot id is provided")

        if values.get("robot_secret") and not values.get("robot_id"):
            raise ValueError("Robot id is required when robot secret is provided")

        if values.get("username") and values.get("password"):
            return values
        elif values.get("robot_id") and values.get("robot_secret"):
            return values
        else:
            raise ValueError(
                "Either username and password or robot_id and robot_secret must be provided"
            )


class Authup:
    def __init__(self, settings: Settings = None):
        self.settings = settings if settings else Settings()

    def get_token(self):
        pass

    async def get_token_async(self):
        pass

    def get_user(self, token: str):
        pass

    async def get_user_async(self, token: str):
        pass
