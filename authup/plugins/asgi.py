from starlette.requests import Request
from starlette.responses import Response
from starlette.types import ASGIApp, Receive, Scope, Send

from authup.token import get_user_from_token_async, introspect_token_async


class AuthupASGIMiddleware:
    def __init__(self, app: ASGIApp, authup_url: str, user: bool = False) -> None:
        self.app = app
        self.authup_url = authup_url
        self.user = user

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return

        request = Request(scope)
        try:

            await self.check_request(request)
            await self.app(scope, receive, send)
            return

        except Exception as e:
            response = Response(str(e), status_code=401)
            await response(scope, receive, send)
            return

    async def validate_token(self, token: str):
        introspection_url = f"{self.authup_url}/token/introspect"

        token_introspection = await introspect_token_async(
            token_introspect_url=introspection_url, token=token
        )
        if not token_introspection.active:
            raise Exception("Inactive token")

    async def check_request(self, request: Request):
        auth_header = request.headers.get("Authorization")
        if not auth_header:
            raise Exception("Missing Authorization header")

        token_type, token = auth_header.split(" ")
        if token_type.lower() != "bearer":
            raise Exception(f"Invalid token type: {token_type}")

        await self.validate_token(token)

        if self.user:
            user = await get_user_from_token_async(
                user_url=f"{self.authup_url}/users/@me", token=token
            )
            request.state.user = user.dict()
