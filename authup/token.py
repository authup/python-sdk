import httpx

from authup.schemas import Token


def get_token(
    token_url: str,
    username: str = None,
    password: str = None,
    client_id: str = None,
    client_secret: str = None,
    headers: dict = None,
):
    """
    Get a token from the token url using either username and password or client_id and client_secret
    :param token_url:
    :param username:
    :param password:
    :param client_id:
    :param client_secret:
    :param headers:
    :return:
    """

    data = None

    if not token_url:
        raise ValueError("No token url provided")

    if not username and not client_id:
        raise ValueError("No username or client_id provided")

    if username and client_id:
        raise ValueError("Both username and client_id provided")

    if username and not password:
        raise ValueError("No password provided for username")

    else:
        data = {
            "grant_type": "password",
            "username": username,
            "password": password,
        }

    if client_id and not client_secret:
        raise ValueError("No client_secret provided for client_id")

    else:
        data = {
            "grant_type": "client_credentials",
            "client_id": client_id,
            "client_secret": client_secret,
        }

    r = httpx.post(token_url, data=data, headers=headers)
    r.raise_for_status()
    return Token.parse_raw(r.text)
