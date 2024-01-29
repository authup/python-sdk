from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel

from ..client.types import Client
from ..constants import DomainType
from ..realm.types import Realm
from ..types_base import DomainEventBaseContext


class IdentityProviderProtocol(Enum):
    LDAP = "ldap"
    OAUTH2 = "oauth2"
    OIDC = "oidc"


class IdentityProviderPreset(Enum):
    FACEBOOK = "facebook"
    GITHUB = "github"
    GITLAB = "gitlab"
    GOOGLE = "google"
    PAYPAL = "paypal"
    INSTAGRAM = "instagram"
    STACKOVERFLOW = "stackoverflow"
    TWITTER = "twitter"


class IdentityProvider(BaseModel):
    id: str
    name: str
    slug: str
    protocol: Optional[str] = IdentityProviderProtocol.OAUTH2.value
    preset: Optional[str] = IdentityProviderPreset.GITHUB.value
    enabled: bool = False
    created_at: str = datetime.now().isoformat()
    updated_at: str = datetime.now().isoformat()
    realm_id: str
    realm: Optional[Realm]
    client_id: Optional[str]
    client: Optional[Client]


class IdentityProviderEventContext(DomainEventBaseContext):
    type: str = DomainType.IDENTITY_PROVIDER.value
    data: IdentityProvider


class IdentityProviderCreate(IdentityProvider):
    id: Optional[str]
    pass


class IdentityProviderUpdate(IdentityProvider):
    id: Optional[str]
    updated_at: str = datetime.now().isoformat()
    pass
