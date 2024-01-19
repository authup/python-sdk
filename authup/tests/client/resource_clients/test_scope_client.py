import asyncio
import os
import sys

import pytest

from ....domains.scope.api import ScopeAPI
from ....domains.scope.types import Scope, ScopeCreate, ScopeUpdate

if (
    sys.version_info[0] == 3
    and sys.version_info[1] >= 8
    and sys.platform.startswith("win")
):
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


@pytest.fixture
def scope_client(authup_client):
    return ScopeAPI(Scope, authup_client.http, prefix="scopes")


@pytest.mark.asyncio
async def test_scope_get_many(scope_client):
    scope = await scope_client.create(ScopeCreate(name=os.urandom(8).hex()))

    scopes = await scope_client.get_many()
    assert scopes
    assert isinstance(scopes[0], Scope)

    print(f"\n{[s.id for s in await scope_client.get_many()]}")

    await scope_client.delete(scope.id)


@pytest.mark.asyncio
async def test_scope_get_one(scope_client):
    scope = await scope_client.create(ScopeCreate(name=os.urandom(8).hex()))
    test_scope = await scope_client.get_one(scope.id)
    assert scope
    assert isinstance(scope, Scope)
    assert scope.id == test_scope.id
    assert scope.name == test_scope.name

    await scope_client.delete(scope.id)


@pytest.mark.asyncio
async def test_scope_create(scope_client):
    test_scope = ScopeCreate(name=os.urandom(8).hex())
    scope = await scope_client.create(test_scope)
    assert scope
    assert isinstance(scope, Scope)
    assert scope.name == test_scope.name
    print(f"\nID: {scope.id}")
    print(f"\nName: {scope.name}")
    print(
        f"\nDatetime:\n\tCreated: {test_scope.created_at}\n\tUpdated: {test_scope.updated_at}"
    )

    await scope_client.delete(scope.id)


@pytest.mark.asyncio
async def test_scope_update(scope_client):
    scope = await scope_client.create(ScopeCreate(name=os.urandom(8).hex()))

    updated_name = os.urandom(8).hex()
    test_scope_updated = ScopeUpdate(name=updated_name)
    updated_scope = await scope_client.update(scope.id, test_scope_updated)

    assert updated_scope
    assert isinstance(updated_scope, Scope)
    assert updated_scope.name == updated_name
    print(f"\nID: {scope.id}")
    print(f"\nName:\n\tOriginal: {scope.name}\n\tUpdated: {updated_scope.name}")
    print(
        f"\nDatetime:\n\tCreated: {test_scope_updated.created_at}\n\tUpdated: {test_scope_updated.updated_at}"
    )

    await scope_client.delete(scope.id)


@pytest.mark.asyncio
async def test_scope_delete(scope_client):
    scope = await scope_client.create(ScopeCreate(name=os.urandom(8).hex()))
    deleted_id = await scope_client.delete(scope.id)
    print(f"\nScope generated: id={scope.id}")
    print(f"Delete scope with id={deleted_id}")
    print(
        f"Deleted id in list of current scopes: {deleted_id in [s.id for s in await scope_client.get_many()]}"
    )
    assert deleted_id == scope.id
    assert deleted_id not in [s.id for s in await scope_client.get_many()]
