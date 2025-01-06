from typing import Any, List
from nibol.models.building import Building, BuildingAvailability, BuildingAvailabilityRequest, BuildingRequest
from pydantic import ValidationError


class BuildingApi:
    def __init__(self, client: Any):
        self.client = client

    def list_buildings(self) -> List[Building]:
        """Retrieve list of buildings."""
        response = self.client.request(
            method="GET",
            endpoint="/v1/building",
        )
        return [Building(**building) for building in response]

    def get_building(self, building_id: str) -> Building:
        """Retrieve building details."""
        try:
            request_data = BuildingRequest(building_id=building_id)
            response = self.client.request(
                method="GET",
                endpoint=f"/v1/building/{request_data.building_id}",
            )

            return Building(**response)
        except ValidationError as e:
            print(e)

    def get_building_availability(
        self, building_id: str = None, date: str = None, category: str = None
    ) -> List[BuildingAvailability]:
        """
        Retrieve building availability for a specific date and category.
        """
        try:
            request_data = BuildingAvailabilityRequest(building_id=building_id, date=date, category=category)

            response = self.client.request(
                method="GET",
                endpoint=f"/v1/building/availability/{request_data.building_id}",
                params={
                    "date": request_data.date,
                    "category": request_data.category,
                },
            )

            return [BuildingAvailability(**item) for item in response]
        except ValidationError as e:
            print(e)
