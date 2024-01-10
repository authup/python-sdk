from ...schemas.role import Role, RoleCreate, RoleUpdate
from ..base_resource_client import ResourceClient


class RoleClient(ResourceClient[Role, RoleCreate, RoleUpdate]):
    pass
