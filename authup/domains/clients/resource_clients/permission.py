from ...schemas.permission import Permission, PermissionCreate, PermissionUpdate
from ..base_resource_client import ResourceClient


class PermissionClient(ResourceClient[Permission, PermissionCreate, PermissionUpdate]):
    pass
