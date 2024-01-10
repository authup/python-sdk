from ...schemas.user import User, UserCreate, UserUpdate
from ..base_resource_client import ResourceClient


class UserClient(ResourceClient[User, UserCreate, UserUpdate]):
    pass
