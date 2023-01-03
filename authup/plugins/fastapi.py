from fastapi import FastAPI

from authup.authup import Authup


class AuthupFastAPI(Authup):
    def __init__(
        self,
        app: FastAPI,
        url: str = None,
        username: str = None,
        password: str = None,
        robot_id: str = None,
        robot_secret: str = None,
    ):
        super().__init__(
            url=url,
            username=username,
            password=password,
            robot_id=robot_id,
            robot_secret=robot_secret,
        )
        self.app = app
