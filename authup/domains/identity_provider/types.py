from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel

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
    protocol: Optional[Enum] = IdentityProviderProtocol
    preset: Optional[Enum] = IdentityProviderPreset
    enabled: bool = False
    created_at: str = datetime.now().isoformat()
    updated_at: str = datetime.now().isoformat()
    realm_id: str
    realm: Realm


class IdentityProviderEventContext(DomainEventBaseContext):
    type: str = DomainType.IDENTITY_PROVIDER
    data: IdentityProvider


class IdentityProviderCreate(IdentityProvider):
    id: Optional[str]
    pass


class IdentityProviderUpdate(IdentityProvider):
    id: Optional[str]
    updated_at: str = datetime.now().isoformat()
    pass
