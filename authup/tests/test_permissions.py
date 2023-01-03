import os

import pytest

from authup import Authup
from authup.permissions import check_permissions
from authup.schemas import Permission
from authup.token import introspect_token_async


@pytest.mark.asyncio
async def test_check_permissions():
    url = os.getenv("AUTHUP_URL")
    username = os.getenv("AUTHUP_USERNAME")
    password = os.getenv("AUTHUP_PASSWORD")

    authup = Authup(url=url, username=username, password=password)
    token = await authup.get_token_async()
    assert token

    introspection_result = await introspect_token_async(
        token_introspect_url=authup.settings.token_url + "/introspect",
        token=token.access_token,
    )

    assert introspection_result

    required_permissions = [
        Permission(name="client_add", inverse=False, power=0),
        Permission(name="client_drop", inverse=False, power=0),
        Permission(name="client_edit", inverse=False, power=0),
    ]

    assert check_permissions(introspection_result, required_permissions)

    required_permissions = [
        Permission(name="client_add", inverse=False, power=10000),
    ]

    assert not check_permissions(introspection_result, required_permissions)

    required_permissions = [
        Permission(name="client_add", inverse=True, power=0),
    ]

    assert not check_permissions(introspection_result, required_permissions)

    required_permissions = [
        Permission(name="test_fails", inverse=False, power=10),
    ]

    assert not check_permissions(introspection_result, required_permissions)

    assert check_permissions(introspection_result, [])

    introspection_result.permissions = []

    assert not check_permissions(introspection_result, required_permissions)
