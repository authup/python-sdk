from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from ...constants import DomainType
from ...realm.types import Realm
from ...role.types import Role
from ...types_base import DomainEventBaseContext
from ..types import IdentityProvider


class IdentityProviderRole(BaseModel):
    id: str
    external_id: str
    created_at: str = datetime.now().isoformat()
    updated_at: str = datetime.now().isoformat()
    role_id: str
    role: Role
    role_realm_id: Optional[str]
    role_realm: Optional[Realm]
    provider_id: str
    provider: IdentityProvider
    provider_realm_id: Optional[str]
    provider_realm: Optional[Realm]


class IdentityProviderRoleEventContext(DomainEventBaseContext):
    type: str = DomainType.IDENTITY_PROVIDER_ROLE
    data: IdentityProviderRole


class IdentityProviderRoleCreate(IdentityProviderRole):
    id: Optional[str]
    pass


class IdentityProviderRoleUpdate(IdentityProviderRole):
    id: Optional[str]
    pass
