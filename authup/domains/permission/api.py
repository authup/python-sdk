from ..base_api_client import ResourceClient
from .types import Permission, PermissionCreate, PermissionUpdate


class PermissionAPI(ResourceClient[Permission, PermissionCreate, PermissionUpdate]):
    pass
