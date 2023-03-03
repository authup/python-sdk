from authup.client.base_resource_client import ResourceClient
from authup.schemas.oauth_2 import OAuth2JsonWebKey, OAuthOpenIDProviderMetadata
from authup.schemas.realm import Realm, RealmCreate, RealmUpdate


class RealmClient(ResourceClient[Realm, RealmCreate, RealmUpdate]):
    async def open_id_configuration(self, realm_id: str) -> OAuthOpenIDProviderMetadata:
        url = self._format_url(realm_id)
        response = await self.client.get(f"{url}/.well-known/openid-configuration")
        response.raise_for_status()
        return OAuthOpenIDProviderMetadata.parse_raw(response.content)

    async def open_id_configuration_jwks(self, realm_id: str) -> OAuth2JsonWebKey:
        response = await self.client.get(f"{self._format_url(realm_id)}/jwks")
        response.raise_for_status()
        return OAuth2JsonWebKey.parse_raw(response.content)
