import asyncio
import os
import sys

import pytest

from ....domains.clients.resource_clients.client import ClientClient
from ....domains.schemas.client import Client, ClientCreate, ClientUpdate

if (
    sys.version_info[0] == 3
    and sys.version_info[1] >= 8
    and sys.platform.startswith("win")
):
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


@pytest.fixture
def client_client(authup_client):
    return ClientClient(Client, authup_client.http, prefix="clients")


@pytest.mark.asyncio
async def test_client_get_many(client_client):
    clients = await client_client.get_many()
    assert clients
    assert isinstance(clients[0], Client)

    print(f"\n{[u.id for u in await client_client.get_many()]}")


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
        f"Deleted id in list of current clients: {deleted_id in [u.id for u in await client_client.get_many()]}"
    )
    assert deleted_id == client.id
    assert deleted_id not in [u.id for u in await client_client.get_many()]
