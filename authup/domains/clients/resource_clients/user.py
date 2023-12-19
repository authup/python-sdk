from authup.domains.clients.base_resource_client import ResourceClient
from authup.domains.schemas.user import User, UserCreate, UserUpdate


class UserClient(ResourceClient[User, UserCreate, UserUpdate]):
    pass
