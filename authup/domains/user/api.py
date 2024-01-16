from ..base_api_client import ResourceClient
from .types import User, UserCreate, UserUpdate


class UserAPI(ResourceClient[User, UserCreate, UserUpdate]):
    pass
