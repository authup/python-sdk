import asyncio
import os
import sys

import pytest

from ....domains.client.api import ClientAPI
from ....domains.client.client_scope.api import ClientScopeAPI
from ....domains.client.client_scope.types import ClientScope, ClientScopeCreate
from ....domains.client.types import Client, ClientCreate, ClientUpdate
from ....domains.scope.api import ScopeAPI
from ....domains.scope.types import Scope, ScopeCreate

if (
    sys.version_info[0] == 3
    and sys.version_info[1] >= 8
    and sys.platform.startswith("win")
):
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


@pytest.fixture
def client_client(authup_client):
    return ClientAPI(Client, authup_client.http, prefix="clients")


@pytest.fixture
def client_scope_client(authup_client):
    return ClientScopeAPI(ClientScope, authup_client.http, prefix="client-scopes")


@pytest.fixture
def scope_client(authup_client):
    return ScopeAPI(Scope, authup_client.http, prefix="scopes")


@pytest.mark.asyncio
async def test_client_get_many(client_client):
    clients = await client_client.get_many()
    assert clients
    assert isinstance(clients[0], Client)

    print(f"\n{[c.id for c in await client_client.get_many()]}")


@pytest.mark.asyncio
async def test_client_scope_get_many(client_scope_client):
    client_scopes = await client_scope_client.get_many()
    assert client_scopes
    assert isinstance(client_scopes[0], ClientScope)

    print(f"\n{[cs.id for cs in await client_scope_client.get_many()]}")


@pytest.mark.asyncio
async def test_client_get_one(client_client):
    client = await client_client.create(ClientCreate(name=os.urandom(8).hex()))
    test_client = await client_client.get_one(client.id)
    assert client
    assert isinstance(client, Client)
    assert client.id == test_client.id
    assert client.name == test_client.name

    await client_client.delete(client.id)


@pytest.mark.asyncio
async def test_client_scope_get_one(client_scope_client, client_client, scope_client):
    client = await client_client.create(ClientCreate(name=os.urandom(8).hex()))
    scope = await scope_client.create(ScopeCreate(name=os.urandom(8).hex()))
    client_scope = await client_scope_client.create(
        ClientScopeCreate(client_id=client.id, scope_id=scope.id)
    )
    test_client_scope = await client_scope_client.get_one(client_scope.id)
    assert client_scope
    assert isinstance(client_scope, ClientScope)
    assert client_scope.id == test_client_scope.id
    assert client_scope.client_id == test_client_scope.client_id
    assert client_scope.scope_id == test_client_scope.scope_id

    await client_client.delete(client.id)
    await scope_client.delete(scope.id)


@pytest.mark.asyncio
async def test_client_create(client_client):
    test_client = ClientCreate(name=os.urandom(8).hex())

    client = await client_client.create(test_client)
    assert client
    assert isinstance(client, Client)
    assert client.name == test_client.name
    print(f"\nID: {client.id}")
    print(f"\nName: {client.name}")
    print(
        f"\nDatetime:\n\tCreated: {test_client.created_at}\n\tUpdated: {test_client.updated_at}"
    )

    await client_client.delete(client.id)


@pytest.mark.asyncio
async def test_client_scope_create(client_scope_client, client_client, scope_client):
    client = await client_client.create(ClientCreate(name=os.urandom(8).hex()))
    scope = await scope_client.create(ScopeCreate(name=os.urandom(8).hex()))

    test_client_scope = ClientScopeCreate(client_id=client.id, scope_id=scope.id)

    client_scope = await client_scope_client.create(test_client_scope)
    assert client_scope
    assert isinstance(client_scope, ClientScope)
    assert client_scope.client_id == test_client_scope.client_id
    assert client_scope.scope_id == test_client_scope.scope_id
    print(f"\nID: {client_scope.id}")

    await client_client.delete(client.id)
    await scope_client.delete(scope.id)


@pytest.mark.asyncio
async def test_client_update(client_client):
    client = await client_client.create(ClientCreate(name=os.urandom(8).hex()))

    updated_name = os.urandom(8).hex()
    test_client_updated = ClientUpdate(name=updated_name)
    updated_client = await client_client.update(client.id, test_client_updated)

    assert updated_client
    assert isinstance(updated_client, Client)
    assert updated_client.name == updated_name
    print(f"\nID: {client.id}")
    print(f"\nName:\n\tOriginal: {client.name}\n\tUpdated: {updated_client.name}")
    print(
        f"\nDatetime:\n\tCreated: {test_client_updated.created_at}\n\tUpdated: {test_client_updated.updated_at}"
    )

    await client_client.delete(client.id)


@pytest.mark.asyncio
async def test_client_delete(client_client):
    client = await client_client.create(ClientCreate(name=os.urandom(8).hex()))
    deleted_id = await client_client.delete(client.id)
    print(f"\nClient generated: id={client.id}")
    print(f"Delete client with id={deleted_id}")
    print(
        f"Deleted id in list of current clients: {deleted_id in [c.id for c in await client_client.get_many()]}"
    )
    assert deleted_id == client.id
    assert deleted_id not in [c.id for c in await client_client.get_many()]


@pytest.mark.asyncio
async def test_client_scope_delete(client_scope_client, client_client, scope_client):
    client = await client_client.create(ClientCreate(name=os.urandom(8).hex()))
    scope = await scope_client.create(ScopeCreate(name=os.urandom(8).hex()))
    client_scope = await client_scope_client.create(
        ClientScopeCreate(client_id=client.id, scope_id=scope.id)
    )

    deleted_id = await client_scope_client.delete(client_scope.id)
    print(f"\nClientScope generated: id={client_scope.id}")
    print(f"Delete client scope with id={deleted_id}")
    print(
        f"Deleted id in list of current client scopes: "
        f"{deleted_id in [cs.id for cs in await client_scope_client.get_many()]}"
    )
    assert deleted_id == client_scope.id
    assert deleted_id not in [cs.id for cs in await client_scope_client.get_many()]

    await client_client.delete(client.id)
    await scope_client.delete(scope.id)
