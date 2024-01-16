from ...base_api_client import ResourceClient
from .types import RobotRole, RobotRoleCreate, RobotRoleUpdate


class RobotRoleAPI(ResourceClient[RobotRole, RobotRoleCreate, RobotRoleUpdate]):
    pass
