from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from ..constants import DomainType
from ..realm.types import Realm
from ..types_base import DomainEventBaseContext
from ..user.types import User


class Client(BaseModel):
    id: str
    name: str
    description: Optional[str]
    secret: Optional[str]
    redirect_url: Optional[str]
    grant_types: Optional[str]
    scope: Optional[str]
    base_url: Optional[str]
    root_url: Optional[str]
    is_confidential: bool = False
    created_at: str = datetime.now().isoformat()
    updated_at: str = datetime.now().isoformat()
    realm_id = str
    realm: Optional[Realm]
    user_id: Optional[str]
    user: Optional[User]


class ClientEventContext(DomainEventBaseContext):
    type: str = f"{DomainType.CLIENT}"
    data: Client


class ClientCreate(Client):
    id: Optional[str]
    pass


class ClientUpdate(Client):
    id: Optional[str]
    updated_at = datetime.now().isoformat()
    pass
