from starlette.requests import Request
from starlette.responses import Response
from starlette.types import ASGIApp, Receive, Scope, Send

from authup.token import introspect_token_async


class AuthupASGIMiddleware:
    def __init__(self, app: ASGIApp, authup_url: str) -> None:
        self.app = app
        self.authup_url = authup_url

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return

        request = Request(scope)
        try:

            auth_header = request.headers.get("Authorization")
            if not auth_header:
                raise Exception("Missing Authorization header")

            token_type, token = auth_header.split(" ")
            if token_type.lower() != "bearer":
                raise Exception(f"Invalid token type: {token_type}")

            await self.validate_token(token)
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
