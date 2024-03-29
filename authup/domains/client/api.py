from ..base_api_client import ResourceClient
from .types import Client, ClientCreate, ClientUpdate


class ClientAPI(ResourceClient[Client, ClientCreate, ClientUpdate]):
    pass
