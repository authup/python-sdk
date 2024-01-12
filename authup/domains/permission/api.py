from ..base_api_client import ResourceClient
from ..permission.types import Permission, PermissionCreate, PermissionUpdate


class PermissionClient(ResourceClient[Permission, PermissionCreate, PermissionUpdate]):
    pass
