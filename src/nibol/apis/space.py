from typing import Any
from pydantic import ValidationError
from nibol.models.space import (
    Space,
    SpaceAvailability,
    SpaceAvailabilityRequest,
    SpaceDetails,
    SpaceListRequest,
    SpaceDetailsRequest,
)


class SpaceApi:
    def __init__(self, client: Any):
        self.client = client

    def list_spaces(self, building: str) -> list[Space]:
        try:
            params = SpaceListRequest(building=building).model_dump(by_alias=True)
            response = self.client.request(
                method="GET",
                endpoint="/v1/space/",
                params=params,
            )

            return [Space(**space) for space in response]
        except ValidationError as e:
            print(e)

    def get_space(self, space_id: str) -> SpaceDetails:
        """
        Retrieve the space details
        """
        try:
            SpaceDetailsRequest(space_id=space_id)
            response = self.client.request(
                method="GET",
                endpoint=f"/v1/space/{space_id}",
            )
            return SpaceDetails(**response)
        except ValidationError as e:
            print(e)

    def get_space_availability(self, space_id: str, date: str) -> SpaceAvailability:
        """
        Retrieve availability for a specific space on a specific date.
        """
        try:
            request_data = SpaceAvailabilityRequest.validate_request(space_id=space_id, date=date)

            response = self.client.request(
                method="GET",
                endpoint=f"/v1/space/availability/{request_data.space_id}",
                params={"date": request_data.date},
            )

            if not isinstance(response, list):
                raise TypeError(f"Expected a list in the response, got {type(response).__name__}")

            return [SpaceAvailability(**item) for item in response]
        except ValidationError as e:
            print(e)

    def get_categories(self, space_id: str) -> list[str]:
        """
        Retrieve the categories of map entities for a specific space.
        """
        space = self.get_space(space_id=space_id)
        categories = [entity["category"] for entity in space.map_entities]
        return sorted(set(categories))
