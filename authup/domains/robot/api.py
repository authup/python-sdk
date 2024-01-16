from ..base_api_client import ResourceClient
from .types import Robot, RobotCreate, RobotUpdate


class RobotAPI(ResourceClient[Robot, RobotCreate, RobotUpdate]):
    async def integrity(self, id: str) -> int:
        response = await self.client.get(f"robots/{id}/integrity")
        response.raise_for_status()
        return response.status_code

    pass
