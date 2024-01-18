import asyncio
import os
import sys

import pytest

from ....domains.client.api import ClientAPI
from ....domains.client.types import Client, ClientCreate
from ....domains.identity_provider.api import IdentityProviderAPI
from ....domains.identity_provider.identity_provider_role.api import (
    IdentityProviderRoleAPI,
)
from ....domains.identity_provider.identity_provider_role.types import (
    IdentityProviderRole,
    IdentityProviderRoleCreate,
    IdentityProviderRoleUpdate,
)
from ....domains.identity_provider.types import (
    IdentityProvider,
    IdentityProviderCreate,
    IdentityProviderUpdate,
)
from ....domains.realm.api import RealmAPI
from ....domains.realm.types import Realm, RealmCreate
from ....domains.role.api import RoleAPI
from ....domains.role.types import Role, RoleCreate

if (
    sys.version_info[0] == 3
    and sys.version_info[1] >= 8
    and sys.platform.startswith("win")
):
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


@pytest.fixture
def identity_provider_client(authup_client):
    return IdentityProviderAPI(
        IdentityProvider, authup_client.http, prefix="identity-providers"
    )


@pytest.fixture
def identity_provider_role_client(authup_client):
    return IdentityProviderRoleAPI(
        IdentityProviderRole, authup_client.http, prefix="identity-provider-roles"
    )


@pytest.fixture
def realm_client(authup_client):
    return RealmAPI(Realm, authup_client.http, prefix="realms")


@pytest.fixture
def role_client(authup_client):
    return RoleAPI(Role, authup_client.http, prefix="roles")


@pytest.fixture
def client_client(authup_client):
    return ClientAPI(Client, authup_client.http, prefix="clients")


@pytest.mark.asyncio
async def test_identity_provider_get_many(identity_provider_client):
    identity_providers = await identity_provider_client.get_many()
    assert identity_providers
    assert isinstance(identity_providers[0], IdentityProvider)

    print(f"\n{[ip.id for ip in await identity_provider_client.get_many()]}")


@pytest.mark.asyncio
async def test_identity_provider_role_get_many(identity_provider_role_client):
    identity_provider_roles = await identity_provider_role_client.get_many()
    assert identity_provider_roles
    assert isinstance(identity_provider_roles[0], IdentityProviderRole)

    print(f"\n{[ipr.id for ipr in await identity_provider_role_client.get_many()]}")


@pytest.mark.asyncio
async def test_identity_provider_get_one(
    identity_provider_client, realm_client, client_client
):
    realm = await realm_client.create(RealmCreate(name=os.urandom(8).hex()))
    client = await client_client.create(ClientCreate(name=os.urandom(8).hex()))

    identity_provider = await identity_provider_client.create(
        IdentityProviderCreate(
            name=os.urandom(8).hex(),
            slug=os.urandom(8).hex(),
            realm_id=realm.id,
            client_id=client.id,
        )
    )
    test_identity_provider = await identity_provider_client.get_one(
        identity_provider.id
    )
    assert identity_provider
    assert isinstance(identity_provider, IdentityProvider)
    assert identity_provider.id == test_identity_provider.id
    assert identity_provider.name == test_identity_provider.name

    await realm_client.delete(realm.id)
    await client_client.delete(client.id)


@pytest.mark.asyncio
async def test_identity_provider_role_get_one(
    identity_provider_role_client,
    identity_provider_client,
    realm_client,
    client_client,
    role_client,
):
    realm = await realm_client.create(RealmCreate(name=os.urandom(8).hex()))
    client = await client_client.create(ClientCreate(name=os.urandom(8).hex()))
    identity_provider = await identity_provider_client.create(
        IdentityProviderCreate(
            name=os.urandom(8).hex(),
            slug=os.urandom(8).hex(),
            realm_id=realm.id,
            client_id=client.id,
        )
    )
    role = await role_client.create(
        RoleCreate(name=os.urandom(8).hex(), realm_id=realm.id)
    )
    identity_provider_role = await identity_provider_role_client.create(
        IdentityProviderRoleCreate(
            external_id=os.urandom(8).hex(),
            role_id=role.id,
            provider_id=identity_provider.id,
        )
    )

    test_identity_provider_role = await identity_provider_role_client.get_one(
        identity_provider_role.id
    )
    assert identity_provider_role
    assert isinstance(identity_provider_role, IdentityProviderRole)
    assert identity_provider_role.id == test_identity_provider_role.id
    assert identity_provider_role.role_id == test_identity_provider_role.role_id
    assert identity_provider_role.provider_id == test_identity_provider_role.provider_id

    await realm_client.delete(realm.id)
    await client_client.delete(client.id)


@pytest.mark.asyncio
async def test_identity_provider_create(
    identity_provider_client, realm_client, client_client
):
    realm = await realm_client.create(RealmCreate(name=os.urandom(8).hex()))
    client = await client_client.create(ClientCreate(name=os.urandom(8).hex()))

    test_identity_provider = IdentityProviderCreate(
        name=os.urandom(8).hex(),
        slug=os.urandom(8).hex(),
        realm_id=realm.id,
        client_id=client.id,
    )
    identity_provider = await identity_provider_client.create(test_identity_provider)

    assert identity_provider
    assert isinstance(identity_provider, IdentityProvider)
    assert identity_provider.name == test_identity_provider.name
    print(f"\nID: {identity_provider.id}")
    print(f"\nName: {identity_provider.name}")
    print(
        f"\nDatetime:\n\tCreated: {test_identity_provider.created_at}\n\tUpdated: {test_identity_provider.updated_at}"
    )

    await realm_client.delete(realm.id)
    await client_client.delete(client.id)


@pytest.mark.asyncio
async def test_identity_provider_role_create(
    identity_provider_role_client,
    identity_provider_client,
    realm_client,
    client_client,
    role_client,
):
    realm = await realm_client.create(RealmCreate(name=os.urandom(8).hex()))
    client = await client_client.create(ClientCreate(name=os.urandom(8).hex()))
    identity_provider = await identity_provider_client.create(
        IdentityProviderCreate(
            name=os.urandom(8).hex(),
            slug=os.urandom(8).hex(),
            realm_id=realm.id,
            client_id=client.id,
        )
    )
    role = await role_client.create(
        RoleCreate(name=os.urandom(8).hex(), realm_id=realm.id)
    )
    test_identity_provider_role = IdentityProviderRoleCreate(
        external_id=os.urandom(8).hex(),
        role_id=role.id,
        provider_id=identity_provider.id,
    )
    identity_provider_role = await identity_provider_role_client.create(
        test_identity_provider_role
    )

    assert identity_provider_role
    assert isinstance(identity_provider_role, IdentityProviderRole)
    assert identity_provider_role.external_id == test_identity_provider_role.external_id
    assert identity_provider_role.role_id == test_identity_provider_role.role_id
    assert identity_provider_role.provider_id == test_identity_provider_role.provider_id
    print(f"\nID: {identity_provider_role.id}")

    await realm_client.delete(realm.id)
    await client_client.delete(client.id)


@pytest.mark.asyncio
async def test_identity_provider_update(
    identity_provider_client, realm_client, client_client
):
    realm = await realm_client.create(RealmCreate(name=os.urandom(8).hex()))
    client = await client_client.create(ClientCreate(name=os.urandom(8).hex()))

    slug = os.urandom(8).hex()
    identity_provider = await identity_provider_client.create(
        IdentityProviderCreate(
            name=os.urandom(8).hex(),
            slug=slug,
            realm_id=realm.id,
            client_id=client.id,
        )
    )
    updated_name = os.urandom(8).hex()
    test_identity_provider_updated = IdentityProviderUpdate(
        name=updated_name, slug=slug, realm_id=realm.id, client_id=client.id
    )
    updated_identity_provider = await identity_provider_client.update(
        identity_provider.id, test_identity_provider_updated
    )

    assert updated_identity_provider
    assert isinstance(updated_identity_provider, IdentityProvider)
    assert updated_identity_provider.name == updated_name
    print(f"\nID: {identity_provider.id}")
    print(
        f"\nName:\n\tOriginal: {identity_provider.name}\n\tUpdated: {updated_identity_provider.name}"
    )
    print(
        f"\nDatetime:\n\tCreated: {test_identity_provider_updated.created_at}\n\t"
        f"Updated: {test_identity_provider_updated.updated_at}"
    )

    await realm_client.delete(realm.id)
    await client_client.delete(client.id)


@pytest.mark.asyncio
async def test_identity_provider_role_update(
    identity_provider_role_client,
    identity_provider_client,
    realm_client,
    client_client,
    role_client,
):
    realm = await realm_client.create(RealmCreate(name=os.urandom(8).hex()))
    client = await client_client.create(ClientCreate(name=os.urandom(8).hex()))
    identity_provider = await identity_provider_client.create(
        IdentityProviderCreate(
            name=os.urandom(8).hex(),
            slug=os.urandom(8).hex(),
            realm_id=realm.id,
            client_id=client.id,
        )
    )
    role = await role_client.create(
        RoleCreate(name=os.urandom(8).hex(), realm_id=realm.id)
    )
    identity_provider_role = await identity_provider_role_client.create(
        IdentityProviderRoleCreate(
            external_id=os.urandom(8).hex(),
            role_id=role.id,
            provider_id=identity_provider.id,
        )
    )

    updated_external_id = os.urandom(8).hex()
    test_identity_provider_role_updated = IdentityProviderRoleUpdate(
        external_id=updated_external_id,
        role_id=role.id,
        provider_id=identity_provider.id,
    )
    updated_identity_provider_role = await identity_provider_role_client.update(
        identity_provider_role.id, test_identity_provider_role_updated
    )

    assert updated_identity_provider_role
    assert isinstance(updated_identity_provider_role, IdentityProviderRole)
    assert updated_identity_provider_role.external_id == updated_external_id
    print(
        f"\nExternal ID:\n\tOriginal: {identity_provider_role.external_id}\n\t"
        f"Updated: {updated_identity_provider_role.external_id}"
    )
    print(
        f"\nDatetime:\n\tCreated: {test_identity_provider_role_updated.created_at}\n\t"
        f"Updated: {test_identity_provider_role_updated.updated_at}"
    )

    await realm_client.delete(realm.id)
    await client_client.delete(client.id)


@pytest.mark.asyncio
async def test_client_delete(identity_provider_client, realm_client, client_client):
    realm = await realm_client.create(RealmCreate(name=os.urandom(8).hex()))
    client = await client_client.create(ClientCreate(name=os.urandom(8).hex()))
    identity_provider = await identity_provider_client.create(
        IdentityProviderCreate(
            name=os.urandom(8).hex(),
            slug=os.urandom(8).hex(),
            realm_id=realm.id,
            client_id=client.id,
        )
    )
    deleted_id = await identity_provider_client.delete(identity_provider.id)
    print(f"\nClient generated: id={identity_provider.id}")
    print(f"Delete client with id={deleted_id}")
    print(
        f"Deleted id in list of current clients: "
        f"{deleted_id in [ip.id for ip in await identity_provider_client.get_many()]}"
    )
    assert deleted_id == identity_provider.id
    assert deleted_id not in [ip.id for ip in await identity_provider_client.get_many()]

    await realm_client.delete(realm.id)
    await client_client.delete(client.id)


@pytest.mark.asyncio
async def test_client_scope_delete(
    identity_provider_role_client,
    identity_provider_client,
    realm_client,
    client_client,
    role_client,
):
    realm = await realm_client.create(RealmCreate(name=os.urandom(8).hex()))
    client = await client_client.create(ClientCreate(name=os.urandom(8).hex()))
    identity_provider = await identity_provider_client.create(
        IdentityProviderCreate(
            name=os.urandom(8).hex(),
            slug=os.urandom(8).hex(),
            realm_id=realm.id,
            client_id=client.id,
        )
    )
    role = await role_client.create(
        RoleCreate(name=os.urandom(8).hex(), realm_id=realm.id)
    )
    identity_provider_role = await identity_provider_role_client.create(
        IdentityProviderRoleCreate(
            external_id=os.urandom(8).hex(),
            role_id=role.id,
            provider_id=identity_provider.id,
        )
    )

    deleted_id = await identity_provider_role_client.delete(identity_provider_role.id)
    print(f"\nClientScope generated: id={identity_provider_role.id}")
    print(f"Delete client scope with id={deleted_id}")
    print(
        f"Deleted id in list of current client scopes: "
        f"{deleted_id in [ipr.id for ipr in await identity_provider_role_client.get_many()]}"
    )
    assert deleted_id == identity_provider_role.id
    assert deleted_id not in [
        ipr.id for ipr in await identity_provider_role_client.get_many()
    ]

    await realm_client.delete(realm.id)
    await client_client.delete(client.id)
