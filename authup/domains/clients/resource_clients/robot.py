from ...schemas.robot import Robot, RobotCreate, RobotUpdate
from ..base_resource_client import ResourceClient


class RobotClient(ResourceClient[Robot, RobotCreate, RobotUpdate]):
    async def integrity(self, id: str) -> str:
        response = await self.client.get(f"robots/{id}/integrity")
        response.raise_for_status()
        return id

    pass
