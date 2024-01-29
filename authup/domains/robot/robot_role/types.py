from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from ...constants import DomainType
from ...realm.types import Realm
from ...robot.types import Robot
from ...role.types import Role
from ...types_base import DomainEventBaseContext


class RobotRole(BaseModel):
    id: str
    robot_id: str
    role_id: str
    role: Optional[Role]
    role_realm_id: Optional[str]
    role_realm: Optional[Realm]
    robot: Optional[Robot]
    robot_realm_id: Optional[str]
    robot_realm: Optional[Realm]
    created_at: str = datetime.now().isoformat()
    updated_at: str = datetime.now().isoformat()


class RobotRoleEventContext(DomainEventBaseContext):
    type: str = DomainType.ROBOT_ROLE.value
    data: RobotRole


class RobotRoleCreate(RobotRole):
    id: Optional[str]
    pass
