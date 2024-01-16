from ...base_api_client import ResourceClient
from .types import ClientScope, ClientScopeCreate, ClientScopeUpdate


class ClientScopeAPI(ResourceClient[ClientScope, ClientScopeCreate, ClientScopeUpdate]):
    pass
