from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from ..constants import DomainType
from ..types_base import DomainEventBaseContext
from .realm import Realm
from .user import User


class Client(BaseModel):
    id: Optional[str]
    name: str
    description: Optional[str]
    secret: str
    redirect_url: Optional[str]
    grant_types: Optional[str]
    scope: Optional[str]
    base_url: Optional[str]
    root_url: Optional[str]
    is_confidential: bool
    created_at: str = datetime.now().isoformat()
    updated_at: str = datetime.now().isoformat()
    realm_id = str
    realm: Realm
    user_id: Optional[str]
    user: Optional[User]


class ClientEventContext(DomainEventBaseContext):
    type: str = f"{DomainType.CLIENT}"
    data: Client
