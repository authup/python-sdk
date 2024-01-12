import asyncio
import sys

import pytest

from ....domains.permission.api import PermissionClient
from ....domains.permission.types import (
    Permission,
    PermissionCreate,
    PermissionUpdate,
)
from ....domains.realm.api import RealmClient
from ....domains.realm.types import Realm

if (
    sys.version_info[0] == 3
    and sys.version_info[1] >= 8
    and sys.platform.startswith("win")
):
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


@pytest.fixture
def permission_client(authup_client):
    return PermissionClient(Permission, authup_client.http, prefix="permissions")


@pytest.fixture
def realm_client(authup_client):
    return RealmClient(Realm, authup_client.http, prefix="realms")


@pytest.mark.asyncio
async def test_permission_get_many(permission_client):
    permissions = await permission_client.get_many()
    assert permissions
    assert isinstance(permissions[0], Permission)

    print(f"\n{[(p.name, p.id) for p in await permission_client.get_many()]}")
    # for id in [p.id for p in await permission_client.get_many() if p.name.startswith('test')]:
    #     await permission_client.delete(id)


@pytest.mark.asyncio
async def test_permission_get_one(permission_client):
    permission = await permission_client.create(
        PermissionCreate(name="test_permission")
    )
    test_permission = await permission_client.get_one(permission.id)
    assert permission
    assert isinstance(permission, Permission)
    assert permission.id == test_permission.id
    assert permission.name == test_permission.name

    await permission_client.delete(permission.id)


@pytest.mark.asyncio
async def test_permission_create(permission_client):
    test_permission = PermissionCreate(name="test_permission")
    permission = await permission_client.create(test_permission)
    assert permission
    assert isinstance(permission, Permission)
    assert permission.name == test_permission.name
    print(f"\nID: {permission.id}")
    print(f"\nName: {permission.name}")
    print(
        f"\nDatetime:\n\tCreated: {test_permission.created_at}\n\tUpdated: {test_permission.updated_at}"
    )

    await permission_client.delete(permission.id)


@pytest.mark.asyncio
async def test_permission_update(permission_client):
    permission = await permission_client.create(
        PermissionCreate(name="test_permission")
    )

    updated_name = "test_updated_permission"
    test_permission_updated = PermissionUpdate(name=updated_name)
    updated_permission = await permission_client.update(
        permission.id, test_permission_updated
    )

    assert updated_permission
    assert isinstance(updated_permission, Permission)
    assert updated_permission.name == updated_name
    print(f"\nID: {permission.id}")
    print(
        f"\nName:\n\tOriginal: {permission.name}\n\tUpdated: {updated_permission.name}"
    )
    print(
        f"\nDatetime:\n\tCreated: {test_permission_updated.created_at}\n\tUpdated: {test_permission_updated.updated_at}"
    )

    await permission_client.delete(permission.id)


@pytest.mark.asyncio
async def test_permission_delete(permission_client):
    permission = await permission_client.create(
        PermissionCreate(name="test_permission")
    )
    deleted_id = await permission_client.delete(permission.id)
    print(f"\nPermission generated: id={permission.id}")
    print(f"Delete permission with id={deleted_id}")
    print(
        f"Deleted id in list of current permissions: {deleted_id in [p.id for p in await permission_client.get_many()]}"
    )
    assert deleted_id == permission.id
    assert deleted_id not in [p.id for p in await permission_client.get_many()]
