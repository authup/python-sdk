from ..base_api_client import ResourceClient
from .types import Client, ClientCreate, ClientUpdate


class ClientClient(ResourceClient[Client, ClientCreate, ClientUpdate]):
    pass
