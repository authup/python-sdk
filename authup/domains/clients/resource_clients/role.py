from authup.domains.clients.base_resource_client import ResourceClient
from authup.domains.schemas.role import Role, RoleCreate, RoleUpdate


class RoleClient(ResourceClient[Role, RoleCreate, RoleUpdate]):
    pass
