import requests.auth

from authup import Authup


class AuthupRequests(Authup, requests.auth.AuthBase):
    def __call__(self, r):
        token = self.get_token()
        r.headers["Authorization"] = f"Bearer {token.access_token}"
        return r
