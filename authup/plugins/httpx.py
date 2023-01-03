from httpx import Auth

from authup.plugins.base import AuthupPluginBase


class AuthupHttpx(AuthupPluginBase, Auth):
    def auth_flow(self, request):
        token = self.authup.get_token()
        request.headers["Authorization"] = f"Bearer {token.access_token}"
        yield request


class AuthupHttpxAsync(AuthupPluginBase, Auth):
    async def async_auth_flow(self, request):
        token = await self.authup.get_token_async()
        request.headers["Authorization"] = f"Bearer {token.access_token}"
        yield request
