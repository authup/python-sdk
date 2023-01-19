from httpx import AsyncClient

from authup.plugins.httpx import AuthupHttpx


class AuthupClient:
    http: AsyncClient

    def __init__(
        self,
        authup_url: str,
        username: str = None,
        password: str = None,
        robot_id: str = None,
        robot_secret: str = None,
    ):
        self.url = authup_url
        self.username = username
        self.password = password
        self.robot_id = robot_id
        self.robot_secret = robot_secret
        self.token = None
        self.token_expires_at = None
        self._setup_http()

    def _setup_http(self):
        httpx_auth = AuthupHttpx(
            url=self.url,
            username=self.username,
            password=self.password,
            robot_id=self.robot_id,
            robot_secret=self.robot_secret,
        )
        if not self.url.startswith("http://") and not self.url.startswith("https://"):
            self.url = f"http://{self.url}"
        if self.url.endswith("/"):
            self.url = self.url[:-1]

        client = AsyncClient(base_url=self.url, auth=httpx_auth)
        self.http = client
        return client
