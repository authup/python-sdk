from authup.domains.clients.base_resource_client import ResourceClient
from authup.domains.schemas.realm import Realm, RealmCreate, RealmUpdate


class RealmClient(ResourceClient[Realm, RealmCreate, RealmUpdate]):
    pass
