import datetime
from logging import info, warning

from authup.settings import Settings, validate_check_credentials
from authup.token import TokenResponse, get_token, get_token_async

from pydantic import SecretStr


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
            self._auth_type = validate_check_credentials(
                username=self.settings.username,
                password=self.settings.password.get_secret_value()
                if self.settings.password
                else None,
                robot_id=self.settings.robot_id,
                robot_secret=self.settings.robot_secret.get_secret_value()
                if self.settings.robot_secret
                else None,
            )
        else:
            if not url:
                raise ValueError("No url provided")
            self._auth_type = validate_check_credentials(
                username, password, robot_id, robot_secret
            )
            self.settings = Settings(
                url=url,
                username=username,
                password=SecretStr(password) if password else None,
                robot_id=robot_id,
                robot_secret=SecretStr(robot_secret) if robot_secret else None,
            )

        self.token: TokenResponse | None = None
        self.token_expires_at: datetime.datetime | None = None

    def get_token(self):
        token = get_token(
            **self.settings.dict(),
            password=self.settings.password.get_secret_value()
            if self.settings.password
            else None,
            robot_secret=self.settings.robot_secret.get_secret_value()
            if self.settings.robot_secret
            else None,
        )

        self._set_token_expires_at(token.expires_in)
        return token

    async def get_token_async(self):
        token = await get_token_async(
            **self.settings.dict(),
            password=self.settings.password.get_secret_value()
            if self.settings.password
            else None,
            robot_secret=self.settings.robot_secret.get_secret_value()
            if self.settings.robot_secret
            else None,
        )

        self._set_token_expires_at(token.expires_in)
        return token

    def get_user(self, token: str):
        pass

    async def get_user_async(self, token: str):
        pass

    def _check_token(self):
        if not self.token or self._check_is_expired():
            self.token = self.get_token()

    def _check_is_expired(self) -> bool:
        now = datetime.datetime.now()
        return now > self.token_expires_at

    def _set_token_expires_at(self, delta: int):
        self.token_expires_at = datetime.datetime.now() + datetime.timedelta(
            seconds=delta
        )

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
