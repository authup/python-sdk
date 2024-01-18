from datetime import datetime

from pydantic import BaseModel

from ...constants import DomainType
from ...types_base import DomainEventBaseContext
from ...user.types import User
from ..types import IdentityProvider


class IdentityProviderAccount(BaseModel):
    id: str
    provider_user_id: str
    provider_user_name: str
    provider_user_email: str
    created_at: str = datetime.now().isoformat()
    updated_at: str = datetime.now().isoformat()
    user_id: str
    user: User
    provider_id = str
    provider = IdentityProvider


class IdentityProviderAccountEventContext(DomainEventBaseContext):
    type: str = DomainType.IDENTITY_PROVIDER_ACCOUNT.value
    data: IdentityProviderAccount
