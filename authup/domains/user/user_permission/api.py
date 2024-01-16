from ...base_api_client import ResourceClient
from .types import UserPermission, UserPermissionCreate, UserPermissionUpdate


class UserPermissionAPI(
    ResourceClient[UserPermission, UserPermissionCreate, UserPermissionUpdate]
):
    pass
