from pydantic import BaseModel

from ...base_api_client import ResourceClient
from .types import ClientScope, ClientScopeCreate


class ClientScopeAPI(ResourceClient[ClientScope, ClientScopeCreate, BaseModel]):
    pass
