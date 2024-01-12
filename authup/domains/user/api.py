from ..base_api_client import ResourceClient
from ..user.types import User, UserCreate, UserUpdate


class UserClient(ResourceClient[User, UserCreate, UserUpdate]):
    pass
