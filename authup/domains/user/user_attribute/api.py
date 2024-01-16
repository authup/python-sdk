from ...base_api_client import ResourceClient
from .types import UserAttribute, UserAttributeCreate, UserAttributeUpdate


class UserAttributeAPI(
    ResourceClient[UserAttribute, UserAttributeCreate, UserAttributeUpdate]
):
    pass
