from authup.client.base_resource_client import ResourceClient
from authup.schemas.realm import Realm, RealmCreate, RealmUpdate


class RealmClient(ResourceClient[Realm, RealmCreate, RealmUpdate]):
    pass
