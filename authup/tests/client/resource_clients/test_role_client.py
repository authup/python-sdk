import asyncio
import os
import sys

import pytest

from ....domains.realm.api import RealmAPI
from ....domains.realm.types import Realm, RealmCreate
from ....domains.role.api import RoleAPI
from ....domains.role.types import Role, RoleCreate, RoleUpdate

if (
    sys.version_info[0] == 3
    and sys.version_info[1] >= 8
    and sys.platform.startswith("win")
):
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


@pytest.fixture
def role_client(authup_client):
    return RoleAPI(Role, authup_client.http, prefix="roles")


@pytest.fixture
def realm_client(authup_client):
    return RealmAPI(Realm, authup_client.http, prefix="realms")


@pytest.mark.asyncio
async def test_role_get_many(role_client):
    roles = await role_client.get_many()
    assert roles
    assert isinstance(roles[0], Role)

    print(f"\n{[r.id for r in await role_client.get_many()]}")


@pytest.mark.asyncio
async def test_role_get_one(role_client, realm_client):
    realm = await realm_client.create(RealmCreate(name=os.urandom(8).hex()))
    role = await role_client.create(RoleCreate(name="test_role"))
    test_role = await role_client.get_one(role.id)
    assert role
    assert isinstance(role, Role)
    assert role.id == test_role.id
    assert role.name == test_role.name

    await realm_client.delete(realm.id)


@pytest.mark.asyncio
async def test_role_create(role_client, realm_client):
    realm = await realm_client.create(RealmCreate(name=os.urandom(8).hex()))
    test_role = RoleCreate(name="test_role")

    role = await role_client.create(test_role)
    assert role
    assert isinstance(role, Role)
    assert role.name == test_role.name
    print(f"\nID: {role.id}")
    print(f"\nName: {role.name}")
    print(
        f"\nDatetime:\n\tCreated: {test_role.created_at}\n\tUpdated: {test_role.updated_at}"
    )

    await realm_client.delete(realm.id)


@pytest.mark.asyncio
async def test_role_update(role_client, realm_client):
    realm = await realm_client.create(RealmCreate(name=os.urandom(8).hex()))
    role = await role_client.create(RoleCreate(name="test_role"))

    updated_name = "test_role_updated"
    test_role_updated = RoleUpdate(name=updated_name)
    updated_role = await role_client.update(role.id, test_role_updated)

    assert updated_role
    assert isinstance(updated_role, Role)
    assert updated_role.name == updated_name
    print(f"\nID: {role.id}")
    print(f"\nName:\n\tOriginal: {role.name}\n\tUpdated: {updated_role.name}")
    print(
        f"\nDatetime:\n\tCreated: {test_role_updated.created_at}\n\tUpdated: {test_role_updated.updated_at}"
    )

    await realm_client.delete(realm.id)


@pytest.mark.asyncio
async def test_role_delete(role_client, realm_client):
    realm = await realm_client.create(RealmCreate(name=os.urandom(8).hex()))
    role = await role_client.create(RoleCreate(name="test_updated"))
    deleted_id = await role_client.delete(role.id)
    print(f"\nRole generated: id={role.id}")
    print(f"Delete role with id={deleted_id}")
    print(
        f"Deleted id in list of current roles: {deleted_id in [r.id for r in await role_client.get_many()]}"
    )
    assert deleted_id == role.id
    assert deleted_id not in [r.id for r in await role_client.get_many()]

    await realm_client.delete(realm.id)
