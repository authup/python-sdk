from httpx import Auth

from authup import Authup


class AuthupHttpx(Auth):
    def __init__(
        self,
        url: str,
        username: str = None,
        password: str = None,
        robot_id: str = None,
        robot_secret: str = None,
    ):
        self.authup = Authup(
            url=url,
            username=username,
            password=password,
            robot_id=robot_id,
            robot_secret=robot_secret,
        )

    def sync_auth_flow(self, request):
        token = self.authup.get_token()
        request.headers["Authorization"] = f"Bearer {token.access_token}"
        yield request

    async def async_auth_flow(self, request):
        token = await self.authup.get_token_async()
        request.headers["Authorization"] = f"Bearer {token.access_token}"
        yield request
