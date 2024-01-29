from pydantic import BaseModel

from ...base_api_client import ResourceClient
from .types import UserPermission, UserPermissionCreate


class UserPermissionAPI(
    ResourceClient[UserPermission, UserPermissionCreate, BaseModel]
):
    pass
