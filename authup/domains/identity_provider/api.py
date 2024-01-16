from ..base_api_client import ResourceClient
from .types import IdentityProvider, IdentityProviderCreate, IdentityProviderUpdate


class IdentityProviderAPI(
    ResourceClient[IdentityProvider, IdentityProviderCreate, IdentityProviderUpdate]
):
    def get_authorized_url(self, base_url: str, id: str):
        return f"{base_url}/identity-providers/{id}/authorize-url".replace("//", "/")

    pass
