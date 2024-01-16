from ..base_api_client import ResourceClient
from .types import Scope, ScopeCreate, ScopeUpdate


class ScopeAPI(ResourceClient[Scope, ScopeCreate, ScopeUpdate]):
    pass
