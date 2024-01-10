from ...schemas.realm import Realm, RealmCreate, RealmUpdate
from ..base_resource_client import ResourceClient


class RealmClient(ResourceClient[Realm, RealmCreate, RealmUpdate]):
    pass
