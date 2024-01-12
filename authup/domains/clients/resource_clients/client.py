from ...schemas.client import Client, ClientCreate, ClientUpdate
from ..base_resource_client import ResourceClient


class ClientClient(ResourceClient[Client, ClientCreate, ClientUpdate]):
    pass
