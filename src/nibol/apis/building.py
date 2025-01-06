from typing import Any
from nibol.models.building import BuildingListResponse, Building


class BuildingApi:
    def __init__(self, client: Any):
        self.client = client

    async def list_buildings(self) -> BuildingListResponse:
        """Retrieve a list of buildings."""
        response = await self.client.request(method="GET", endpoint="/v1/building/")
        return BuildingListResponse(__root__=response)

    async def get_building(self, building_id: str) -> Building:
        """Retrieve building details."""
        response = await self.client.request(method="GET", endpoint=f"/v1/building/{building_id}")
        return Building(**response)
