from pydantic import BaseModel

from ...base_api_client import ResourceClient
from .types import RobotRole, RobotRoleCreate


class RobotRoleAPI(ResourceClient[RobotRole, RobotRoleCreate, BaseModel]):
    pass
