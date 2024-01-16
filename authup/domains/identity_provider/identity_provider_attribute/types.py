from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from ...constants import DomainType
from ...types_base import DomainEventBaseContext
from ..types import IdentityProvider


class IdentityProviderAttribute(BaseModel):
    id: str
    name: str
    value: Optional[str]
    provider_id: str
    provider: IdentityProvider
    created_at: str = datetime.now().isoformat()
    updated_at: str = datetime.now().isoformat()


class IdentityProviderAttributeEventContext(DomainEventBaseContext):
    type: str = DomainType.IDENTITY_PROVIDER_ATTRIBUTE
    data: IdentityProviderAttribute
