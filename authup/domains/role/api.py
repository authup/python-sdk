from ..base_api_client import ResourceClient
from .types import Role, RoleCreate, RoleUpdate


class RoleAPI(ResourceClient[Role, RoleCreate, RoleUpdate]):
    pass
