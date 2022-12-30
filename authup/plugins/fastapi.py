from fastapi import FastAPI

from authup.authup import Authup


class FastAPIPlugin:
    def __init__(self, app: FastAPI, authup: Authup):
        self.app = app
        self.authup = authup

