import os

import pytest

from authup import Authup
from authup.permissions import check_permissions
from authup.schemas.token import Permission
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

    check_permissions(introspection_result.permissions, required_permissions)

    required_permissions = [
        Permission(name="client_add", inverse=False, power=10000),
    ]

    with pytest.raises(Exception):
        check_permissions(introspection_result.permissions, required_permissions)

    required_permissions = [
        Permission(name="client_add", inverse=True, power=0),
    ]
    with pytest.raises(Exception):
        check_permissions(introspection_result.permissions, required_permissions)

    required_permissions = [
        Permission(name="test_fails", inverse=False, power=10),
    ]
    with pytest.raises(Exception):
        check_permissions(introspection_result.permissions, required_permissions)

    check_permissions(introspection_result.permissions, [])

    introspection_result.permissions = []

    with pytest.raises(Exception):
        check_permissions(introspection_result.permissions, required_permissions)
