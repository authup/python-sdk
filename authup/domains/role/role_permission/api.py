from pydantic import BaseModel

from ...base_api_client import ResourceClient
from .types import RolePermission, RolePermissionCreate


class RolePermissionAPI(
    ResourceClient[RolePermission, RolePermissionCreate, BaseModel]
):
    pass
