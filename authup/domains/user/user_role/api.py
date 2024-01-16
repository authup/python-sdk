from ...base_api_client import ResourceClient
from .types import UserRole, UserRoleCreate, UserRoleUpdate


class UserRoleAPI(ResourceClient[UserRole, UserRoleCreate, UserRoleUpdate]):
    pass
