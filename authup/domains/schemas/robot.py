from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from ..constants import DomainType
from ..types_base import DomainEventBaseContext
from .realm import Realm


class Robot(BaseModel):
    id: str
    secret: Optional[str]
    name: str
    description: Optional[str]
    active: bool = False
    created_at: str = datetime.now().isoformat()
    updated_at: str = datetime.now().isoformat()
    user_id: Optional[str]
    user: Optional[str]
    realm_id: str
    realm: Optional[Realm]


class RobotEventContext(DomainEventBaseContext):
    type: str = f"{DomainType.ROBOT}"
    data: Robot


class RobotCreate(Robot):
    id: Optional[str]
    pass


class RobotUpdate(Robot):
    id: Optional[str]
    updated_at: str = datetime.now().isoformat()
    pass


ROBOT_SYSTEM_NAME = "SYSTEM"
