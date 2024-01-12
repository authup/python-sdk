import asyncio
import os
import sys

import pytest

from ....domains.realm.api import RealmClient
from ....domains.realm.types import Realm, RealmCreate
from ....domains.user.api import UserClient
from ....domains.user.types import User, UserCreate, UserUpdate

if (
    sys.version_info[0] == 3
    and sys.version_info[1] >= 8
    and sys.platform.startswith("win")
):
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


@pytest.fixture
def user_client(authup_client):
    return UserClient(User, authup_client.http, prefix="users")


@pytest.fixture
def realm_client(authup_client):
    return RealmClient(Realm, authup_client.http, prefix="realms")


@pytest.mark.asyncio
async def test_user_get_many(user_client):
    users = await user_client.get_many()
    assert users
    assert isinstance(users[0], User)

    print(f"\n{[u.id for u in await user_client.get_many()]}")


@pytest.mark.asyncio
async def test_user_get_one(user_client, realm_client):
    realm = await realm_client.create(RealmCreate(name=os.urandom(8).hex()))
    user = await user_client.create(
        UserCreate(name=os.urandom(8).hex(), display_name="test", realm_id=realm.id)
    )
    test_user = await user_client.get_one(user.id)
    assert user
    assert isinstance(user, User)
    assert user.id == test_user.id
    assert user.name == test_user.name

    await realm_client.delete(realm.id)


@pytest.mark.asyncio
async def test_user_create(user_client, realm_client):
    realm = await realm_client.create(RealmCreate(name=os.urandom(8).hex()))
    test_user = UserCreate(
        name=os.urandom(8).hex(), display_name="test", realm_id=realm.id
    )

    user = await user_client.create(test_user)
    assert user
    assert isinstance(user, User)
    assert user.name == test_user.name
    print(f"\nID: {user.id}")
    print(f"\nName: {user.name}")
    print(
        f"\nDatetime:\n\tCreated: {test_user.created_at}\n\tUpdated: {test_user.updated_at}"
    )

    await realm_client.delete(realm.id)


@pytest.mark.asyncio
async def test_user_update(user_client, realm_client):
    realm = await realm_client.create(RealmCreate(name=os.urandom(8).hex()))
    user = await user_client.create(
        UserCreate(name=os.urandom(8).hex(), display_name="test", realm_id=realm.id)
    )

    updated_name = os.urandom(8).hex()
    test_user_updated = UserUpdate(name=updated_name, display_name=user.display_name)
    updated_user = await user_client.update(user.id, test_user_updated)

    assert updated_user
    assert isinstance(updated_user, User)
    assert updated_user.name == updated_name
    print(f"\nID: {user.id}")
    print(f"\nName:\n\tOriginal: {user.name}\n\tUpdated: {updated_user.name}")
    print(
        f"\nDatetime:\n\tCreated: {test_user_updated.created_at}\n\tUpdated: {test_user_updated.updated_at}"
    )

    await realm_client.delete(realm.id)


@pytest.mark.asyncio
async def test_user_delete(user_client, realm_client):
    realm = await realm_client.create(RealmCreate(name=os.urandom(8).hex()))
    user = await user_client.create(
        UserCreate(name=os.urandom(8).hex(), display_name="test", realm_id=realm.id)
    )
    deleted_id = await user_client.delete(user.id)
    print(f"\nUser generated: id={user.id}")
    print(f"Delete user with id={deleted_id}")
    print(
        f"Deleted id in list of current users: {deleted_id in [u.id for u in await user_client.get_many()]}"
    )
    assert deleted_id == user.id
    assert deleted_id not in [u.id for u in await user_client.get_many()]

    await realm_client.delete(realm.id)
