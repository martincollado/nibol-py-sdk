from typing import Optional, Any
from nibol.models.space import SpaceListResponse, SpaceDetails


class SpaceApi:
    def __init__(self, client: Any):
        self.client = client

    async def list_spaces(self, building_id: Optional[str] = None) -> SpaceListResponse:
        """Retrieve a list of spaces."""
        params = {"building": building_id} if building_id else {}
        response = await self.client.request(
            method="GET", endpoint="/v1/space/", params=params
        )
        return SpaceListResponse(__root__=response)

    async def get_space(self, space_id: str) -> SpaceDetails:
        """Retrieve space details."""
        response = await self.client.request(
            method="GET", endpoint=f"/v1/space/{space_id}"
        )
        return SpaceDetails(**response)
