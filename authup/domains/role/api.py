from ..base_api_client import ResourceClient
from ..role.types import Role, RoleCreate, RoleUpdate


class RoleClient(ResourceClient[Role, RoleCreate, RoleUpdate]):
    pass
