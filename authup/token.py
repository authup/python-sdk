import httpx

from authup.schemas.token import TokenIntrospectionResponse, TokenResponse
from authup.schemas.user import User
from authup.settings import CredentialTypes, validate_check_credentials


def get_token(
    token_url: str,
    username: str = None,
    password: str = None,
    robot_id: str = None,
    robot_secret: str = None,
    headers: dict = None,
) -> TokenResponse:
    """
    Get a token from the token url using either username and password or client_id and robot_secret
    :param token_url:
    :param username:
    :param password:
    :param robot_id:
    :param robot_secret:
    :param headers:
    :return:
    """

    if not token_url:
        raise ValueError("No token url provided")
    # make sure we have either username and password or client_id and robot_secret
    data = _make_token_data(username, password, robot_id, robot_secret)

    r = httpx.post(token_url, data=data, headers=headers)
    r.raise_for_status()
    return TokenResponse.parse_raw(r.content)


async def refresh_token_async(token_url: str, refresh_token: str) -> TokenResponse:
    """
    Use a refresh token to get a new token
    :param token_url: the url to get the token from
    :param refresh_token: the refresh token from a previous token
    :return: TokenResponse with the new token
    """
    async with httpx.AsyncClient() as client:
        r = await client.post(
            token_url,
            data={"grant_type": "refresh_token", "refresh_token": refresh_token},
        )
        print(r.content)
    r.raise_for_status()

    return TokenResponse.parse_raw(r.content)


def refresh_token(token_url: str, refresh_token: str) -> TokenResponse:
    """
    Use a refresh token to get a new token
    :param token_url: the url to get the token from
    :param refresh_token: the refresh token from a previous token
    :return: TokenResponse with the new token
    """
    r = httpx.post(
        token_url, data={"grant_type": "refresh_token", "refresh_token": refresh_token}
    )
    r.raise_for_status()
    return TokenResponse.parse_raw(r.content)


async def get_token_async(
    token_url: str,
    username: str = None,
    password: str = None,
    robot_id: str = None,
    robot_secret: str = None,
    headers: dict = None,
) -> TokenResponse:
    """
    Get a token from the token url using either username and password or client_id and robot_secret
    :param token_url:
    :param username:
    :param password:
    :param robot_id:
    :param robot_secret:
    :param headers:
    :return:
    """

    if not token_url:
        raise ValueError("No token url provided")
    # make sure we have either username and password or client_id and robot_secret
    data = _make_token_data(username, password, robot_id, robot_secret)

    async with httpx.AsyncClient() as client:
        r = await client.post(token_url, data=data, headers=headers)
    r.raise_for_status()

    return TokenResponse.parse_raw(r.content)


async def get_user_from_token_async(user_url: str, token: str) -> User:
    async with httpx.AsyncClient() as client:
        r = await client.get(url=user_url, headers={"Authorization": f"Bearer {token}"})
    r.raise_for_status()
    return User.parse_raw(r.content)


def get_user_from_token(user_url: str, token: str) -> User:
    r = httpx.get(url=user_url, headers={"Authorization": f"Bearer {token}"})
    r.raise_for_status()
    return User.parse_raw(r.content)


async def introspect_token_async(
    token_introspect_url: str,
    token: str,
    headers: dict = None,
) -> TokenIntrospectionResponse:
    """
    Validate a token by sending it to the token url
    :param token_introspect_url:
    :param token:
    :param headers:
    :return:
    """

    if not token_introspect_url:
        raise ValueError("No token url provided")
    if not token:
        raise ValueError("No token provided")

    async with httpx.AsyncClient() as client:
        r = await client.post(
            token_introspect_url, headers=headers, data={"token": token}
        )

    r.raise_for_status()

    return TokenIntrospectionResponse.parse_raw(r.content)


def introspect_token(
    token_introspect_url: str,
    token: str,
    headers: dict = None,
) -> TokenIntrospectionResponse:
    """
    Validate a token by sending it to the token url
    :param token_introspect_url:
    :param token:
    :param headers:
    :return:
    """

    if not token_introspect_url:
        raise ValueError("No token url provided")
    if not token:
        raise ValueError("No token provided")

    r = httpx.post(token_introspect_url, headers=headers, data={"token": token})

    r.raise_for_status()

    return TokenIntrospectionResponse.parse_raw(r.content)


def _make_token_data(
    username: str = None,
    password: str = None,
    robot_id: str = None,
    robot_secret: str = None,
) -> dict:

    # check if we have username and password or client_id and robot_secret
    credential_type = validate_check_credentials(
        username, password, robot_id, robot_secret
    )

    # create request data according to the credential type
    if credential_type == CredentialTypes.user:
        return {
            "grant_type": "password",
            "username": username,
            "password": password,
        }

    else:
        return {
            "grant_type": "robot_credentials",
            "id": robot_id,
            "secret": robot_secret,
        }
