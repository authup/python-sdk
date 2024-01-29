from pydantic import BaseModel

from ...base_api_client import ResourceClient
from .types import UserRole, UserRoleCreate


class UserRoleAPI(ResourceClient[UserRole, UserRoleCreate, BaseModel]):
    pass
