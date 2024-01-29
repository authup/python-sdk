from ...base_api_client import ResourceClient
from .types import RoleAttribute, RoleAttributeCreate, RoleAttributeUpdate


class RoleAttributeAPI(
    ResourceClient[RoleAttribute, RoleAttributeCreate, RoleAttributeUpdate]
):
    pass
