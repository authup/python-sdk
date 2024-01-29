from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel

from ..realm.types import Realm


class KeyType(Enum):
    OCT = "oct"
    RSA = "rsa"
    EC = "ec"


class Key(BaseModel):
    id: str
    type: str
    signature_algorithm: str
    priority: int
    decryption_key: Optional[str]
    encryption_key: Optional[str]
    created_at: str = datetime.now().isoformat()
    updated_at: str = datetime.now().isoformat()
    realm_id: str
    realm: Realm
