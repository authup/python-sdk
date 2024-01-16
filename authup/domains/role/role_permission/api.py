from ...base_api_client import ResourceClient
from .types import RolePermission, RolePermissionCreate, RolePermissionUpdate


class RolePermissionAPI(
    ResourceClient[RolePermission, RolePermissionCreate, RolePermissionUpdate]
):
    pass
