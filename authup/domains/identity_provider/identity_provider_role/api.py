from ...base_api_client import ResourceClient
from .types import (
    IdentityProviderRole,
    IdentityProviderRoleCreate,
    IdentityProviderRoleUpdate,
)


class IdentityProviderRoleAPI(
    ResourceClient[
        IdentityProviderRole, IdentityProviderRoleCreate, IdentityProviderRoleUpdate
    ]
):
    pass
