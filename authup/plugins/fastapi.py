from fastapi import FastAPI, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials


class FastAPIPlugin:
    def __init__(self, app: FastAPI, authup: AuthUp):
        self.app = app
        self.authup = authup

        self.app.add_middleware(
            AuthUpMiddleware,
            authup=self.authup,
        )

        self.app.add_exception_handler(
            AuthUpException,
            self.handle_authup_exception,
        )

    def handle_authup_exception(
        self, request: Request, exc: AuthUpException
    ) -> JSONResponse:
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "error": exc.error,
                "message": exc.message,
            },
        )
