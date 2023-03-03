from typing import List, Optional

from pydantic import BaseModel


class OAuthOpenIDProviderMetadata(BaseModel):
    issuer: str
    authorization_endpoint: str
    service_documentation: Optional[str] = None
    registration_endpoint: Optional[str] = None
    userinfo_endpoint: Optional[str] = None
    introspection_endpoint: str
    token_endpoint: str
    revocation_endpoint: str
    jwks_uri: str
    response_types_supported: Optional[List[str]] = None
    subject_types_supported: List[str]
    id_token_signing_alg_values_supported: List[str]


class OAuth2JsonWebKey(BaseModel):
    y: Optional[str] = None
    x: Optional[str] = None
    qi: Optional[str] = None
    q: Optional[str] = None
    p: Optional[str] = None
    n: Optional[str] = None
    kty: Optional[str] = None
    k: Optional[str] = None
    e: Optional[str] = None
    dq: Optional[str] = None
    dp: Optional[str] = None
    d: Optional[str] = None
    crv: Optional[str] = None
    kid: Optional[str] = None
    alg: Optional[str] = None
