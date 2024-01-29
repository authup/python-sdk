from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel

from ..constants import DomainType
from ..realm.types import Realm
from ..types_base import DomainEventBaseContext


class ScopeName(Enum):
    GLOBAL = "global"
    OPEN_ID = "openid"
    EMAIL = "email"
    ROLES = "roles"
    IDENTITY = "identity"


class Scope(BaseModel):
    id: str
    built_in: bool = False
    name: str
    description: Optional[str]
    realm_id: Optional[str]
    realm: Optional[Realm]
    created_at: str = datetime.now().isoformat()
    updated_at: str = datetime.now().isoformat()


class ScopeEventContext(DomainEventBaseContext):
    type: str = DomainType.SCOPE.value
    data: Scope


class ScopeCreate(Scope):
    id: Optional[str]
    pass


class ScopeUpdate(Scope):
    id: Optional[str]
    updated_at: str = datetime.now().isoformat()
    pass
