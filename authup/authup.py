from pydantic import BaseSettings, Field
from httpx import AsyncClient, Client


class Settings(BaseSettings):
    robot_id: str = Field(..., env="ROBOT_ID")
    robot_secret: str = Field(..., env="ROBOT_SECRET")
    url: str = Field(..., env="URL")
    username: str = Field(..., env="USERNAME")
    password: str = Field(..., env="PASSWORD")

    class Config:
        env_prefix = "AUTHUP_"
        env_file = ".env"

    @property
    def token_url(self):
        return f"{self.url}/token"

    @property
    def user_url(self):
        return f"{self.url}/users"


class Authup:
    def __init__(self, settings: Settings):
        self.settings = settings

    def get_token(self):
        pass

    async def get_token_async(self):
        pass

    def get_user(self, token: str):
        pass

    async def get_user_async(self, token: str):
        pass
