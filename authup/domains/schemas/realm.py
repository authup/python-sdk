from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from authup.domains.constants import DomainType
from authup.domains.types_base import DomainEventBaseContext


class Realm(BaseModel):
    id: Optional[str]
    name: str
    description: Optional[str] = None
    built_in: bool
    created_at: datetime
    updated_at: datetime


class RealmEventContext(DomainEventBaseContext):
    type: str = f"{DomainType.REALM}"
    data: Realm


class RealmCreate(Realm):
    pass


class RealmUpdate(Realm):
    pass
