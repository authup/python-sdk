import asyncio
import os
import sys

import pytest

from ....domains.realm.api import RealmAPI
from ....domains.realm.types import Realm, RealmCreate, RealmUpdate

if (
    sys.version_info[0] == 3
    and sys.version_info[1] >= 8
    and sys.platform.startswith("win")
):
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


@pytest.fixture
def realm_client(authup_client):
    return RealmAPI(Realm, authup_client.http, prefix="realms")


@pytest.mark.asyncio
async def test_realm_get_many(realm_client):
    realms = await realm_client.get_many()
    assert realms
    assert isinstance(realms[0], Realm)

    print(f"\n{[r.id for r in await realm_client.get_many()]}")


@pytest.mark.asyncio
async def test_realm_get_one(realm_client):
    realm = await realm_client.create(RealmCreate(name=os.urandom(8).hex()))
    test_realm = await realm_client.get_one(realm.id)
    assert realm
    assert isinstance(realm, Realm)
    assert realm.id == test_realm.id
    assert realm.name == test_realm.name

    await realm_client.delete(realm.id)


@pytest.mark.asyncio
async def test_realm_create(realm_client):
    test_realm = RealmCreate(name=os.urandom(8).hex())
    realm = await realm_client.create(test_realm)
    assert realm
    assert isinstance(realm, Realm)
    assert realm.name == test_realm.name
    print(f"\nID: {realm.id}")
    print(f"\nName: {realm.name}")
    print(
        f"\nDatetime:\n\tCreated: {test_realm.created_at}\n\tUpdated: {test_realm.updated_at}"
    )

    await realm_client.delete(realm.id)


@pytest.mark.asyncio
async def test_realm_update(realm_client):
    realm = await realm_client.create(RealmCreate(name=os.urandom(8).hex()))

    updated_name = os.urandom(8).hex()
    test_realm_updated = RealmUpdate(name=updated_name)
    updated_realm = await realm_client.update(realm.id, test_realm_updated)

    assert updated_realm
    assert isinstance(updated_realm, Realm)
    assert updated_realm.name == updated_name
    print(f"\nID: {realm.id}")
    print(f"\nName:\n\tOriginal: {realm.name}\n\tUpdated: {updated_realm.name}")
    print(
        f"\nDatetime:\n\tCreated: {test_realm_updated.created_at}\n\tUpdated: {test_realm_updated.updated_at}"
    )

    await realm_client.delete(realm.id)


@pytest.mark.asyncio
async def test_realm_delete(realm_client):
    realm = await realm_client.create(RealmCreate(name=os.urandom(8).hex()))
    deleted_id = await realm_client.delete(realm.id)
    print(f"\nRealm generated: id={realm.id}")
    print(f"Delete realm with id={deleted_id}")
    print(
        f"Deleted id in list of current realms: {deleted_id in [r.id for r in await realm_client.get_many()]}"
    )
    assert deleted_id == realm.id
    assert deleted_id not in [r.id for r in await realm_client.get_many()]
