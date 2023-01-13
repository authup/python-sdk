import pytest

from authup.client.resource_clients.realm import RealmClient
from authup.schemas.realm import Realm


@pytest.fixture
def realm_client(authup_client):
    return RealmClient(Realm, authup_client.http, prefix="/realms")


@pytest.mark.asyncio
async def test_realm_list(realm_client):
    realms = await realm_client.get_many()
    assert realms
    assert isinstance(realms[0], Realm)

    print(realm_client.get_many)

    # sync_realms = realm_client.get_many.sync()
