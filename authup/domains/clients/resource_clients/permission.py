from authup.domains.clients.base_resource_client import ResourceClient
from authup.domains.schemas.permission import Permission, PermissionCreate, PermissionUpdate


class PermissionClient(ResourceClient[Permission, PermissionCreate, PermissionUpdate]):
    pass
