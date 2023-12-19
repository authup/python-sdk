from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from authup.domains.types_base import DomainEventBaseContext
from authup.domains.constants import DomainType


class Realm(BaseModel):
    id: str
    name: str
    description: Optional[str] = None
    built_in: bool
    created_at: datetime
    updated_at: datetime


class RealmEventContext(DomainEventBaseContext):
    type: str  # f'{DomainType.REALM}'
    data: Realm


class RealmCreate(Realm):
    pass


class RealmUpdate(Realm):
    pass
