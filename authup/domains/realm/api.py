from ..base_api_client import ResourceClient
from ..realm.types import Realm, RealmCreate, RealmUpdate


class RealmClient(ResourceClient[Realm, RealmCreate, RealmUpdate]):
    pass
