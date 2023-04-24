import os

import requests

from authup.plugins.requests import AuthupRequests


def test_requests_auth():
    url = os.getenv("AUTHUP_URL")
    authup = AuthupRequests(
        url=url,
        username=os.getenv("AUTHUP_USERNAME"),
        password=os.getenv("AUTHUP_PASSWORD"),
    )
    r = requests.get(f"{url}/users/@me", auth=authup)
    assert r.status_code == 200
