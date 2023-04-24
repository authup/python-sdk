import os

from authup.client import AuthupClient


def test_init():
    url = os.getenv("AUTHUP_URL")
    username = os.getenv("AUTHUP_USERNAME")
    password = os.getenv("AUTHUP_PASSWORD")
    client = AuthupClient(authup_url=url, username=username, password=password)
    assert client

    assert client.url == url
    assert client.username == username

    assert client.http.base_url == url

    client = AuthupClient(
        authup_url="localhost:3010", username=username, password=password
    )
    assert client.http.base_url == "http://localhost:3010"

    client = AuthupClient(
        authup_url="localhost:3010/", username=username, password=password
    )
    assert client.http.base_url == "http://localhost:3010"
