from ..base_api_client import ResourceClient
from .types import Realm, RealmCreate, RealmUpdate


class RealmAPI(ResourceClient[Realm, RealmCreate, RealmUpdate]):
    pass
