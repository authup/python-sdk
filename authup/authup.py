import datetime
from typing import Union

from authup.schemas.token import TokenResponse
from authup.schemas.user import User
from authup.settings import CredentialTypes, Settings, validate_check_credentials
from authup.token import (
    get_token,
    get_token_async,
    get_user_from_token,
    get_user_from_token_async,
)


class Authup:
    def __init__(
        self,
        url: str = None,
        username: str = None,
        password: str = None,
        robot_id: str = None,
        robot_secret: str = None,
        settings: Settings = None,
    ):
        if settings:
            self.settings = settings
            self._auth_type = (
                CredentialTypes.user
                if self.settings.username
                else CredentialTypes.robot
            )
        else:
            if not url:
                raise ValueError("No url provided")
            self._auth_type = validate_check_credentials(
                username, password, robot_id, robot_secret
            )

            if self._auth_type == CredentialTypes.user:
                self.settings = Settings(
                    url=url,
                    username=username,
                    password=password,
                    robot_id=None,
                    robot_secret=None,
                )
            else:
                self.settings = Settings(
                    url=url,
                    username=None,
                    password=None,
                    robot_id=robot_id,
                    robot_secret=robot_secret,
                )

        self.token: Union[TokenResponse, None] = None
        self.token_expires_at: Union[datetime.datetime, None] = None

    def get_token(self) -> TokenResponse:
        """
        Get a new token from the authup server and set the token and token_expires_at attributes
        :return:
        """

        self.token = self._get_token()
        self._set_token_expires_at(self.token.expires_in)
        return self.token

    def _get_token(self):
        if not self._is_expired():
            return self.token

        if self._auth_type == CredentialTypes.user:
            token = get_token(
                token_url=self.settings.token_url,
                username=self.settings.username,
                password=self.settings.password.get_secret_value(),
            )
        else:
            token = get_token(
                token_url=self.settings.token_url,
                robot_id=self.settings.robot_id,
                robot_secret=self.settings.robot_secret.get_secret_value(),
            )
        return token

    async def get_token_async(self) -> TokenResponse:
        self.token = await self._get_token_async()
        self._set_token_expires_at(self.token.expires_in)
        return self.token

    async def _get_token_async(self):
        if self._auth_type == CredentialTypes.user:
            token = await get_token_async(
                token_url=self.settings.token_url,
                username=self.settings.username,
                password=self.settings.password.get_secret_value(),
            )
        else:
            token = await get_token_async(
                token_url=self.settings.token_url,
                robot_id=self.settings.robot_id,
                robot_secret=self.settings.robot_secret.get_secret_value(),
            )
        return token

    def get_authorization_header(self) -> dict:
        self._check_token()
        return {"Authorization": f"Bearer {self.token.access_token}"}

    def get_user(self, token: str) -> User:
        url = self.settings.user_url + "/@me"
        user = get_user_from_token(url, token)
        return user

    async def get_user_async(self, token: str) -> User:
        url = self.settings.user_url + "/@me"
        user = await get_user_from_token_async(url, token)
        return user

    def _check_token(self):
        # todo use refresh token if available
        if not self.token or self._is_expired():
            self.token = self.get_token()

    def _is_expired(self) -> bool:

        if not self.token_expires_at:
            return True
        now = datetime.datetime.now()
        return now > self.token_expires_at

    def _set_token_expires_at(self, delta: int):
        now = datetime.datetime.now()
        self.token_expires_at = now + datetime.timedelta(seconds=delta)

    def __repr__(self):
        if self.settings.username:
            repr_string = (
                f"Authup(url={self.settings.url}, "
                f"username={self.settings.username}, password={self.settings.password})"
            )
        else:
            repr_string = (
                f"Authup(url={self.settings.url}, "
                f"robot_id={self.settings.robot_id}, robot_secret={self.settings.robot_secret})"
            )
        return repr_string
