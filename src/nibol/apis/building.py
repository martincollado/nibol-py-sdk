from typing import Any, List, Optional, Union, Coroutine
from pydantic import ValidationError
from nibol.models.building import Building, BuildingAvailability, BuildingAvailabilityRequest, BuildingRequest


class BuildingAPI:
    """
    Manages Building operations (list, get, availability) in both sync and async modes.
    """

    def __init__(self, client: Any):
        # Detect if the client is async by looking for `arequest` or a class name
        # that starts with "Async". Keep a log reference if available.
        self.client = client
        self.is_async = hasattr(client, "arequest") or client.__class__.__name__.startswith("Async")
        self.log = getattr(client, "logger", None)

    def _log(self, message: str, **kwargs) -> None:
        if self.log:
            self.log.info(message, **kwargs)

    async def _execute_request_async(self, method: str, endpoint: str, params: Optional[dict] = None) -> Any:
        """Executes an async request using the provided client."""
        try:
            return await self.client.request(method=method, endpoint=endpoint, params=params)
        except Exception as e:
            if self.log:
                self.log.error("unexpected_error", mode="async", endpoint=endpoint, error=str(e))
            raise

    def _execute_request_sync(self, method: str, endpoint: str, params: Optional[dict] = None) -> Any:
        """Executes a sync request using the provided client."""
        try:
            return self.client.request(method=method, endpoint=endpoint, params=params)
        except Exception as e:
            if self.log:
                self.log.error("unexpected_error", mode="sync", endpoint=endpoint, error=str(e))
            raise

    def _request(
        self, method: str, endpoint: str, params: Optional[dict] = None
    ) -> Union[Any, Coroutine[Any, Any, Any]]:
        """
        Dispatches to the correct sync or async method based on `is_async`.
        Returns either the raw response (sync) or an awaitable coroutine (async).
        """
        if self.is_async:
            return self._execute_request_async(method, endpoint, params)
        return self._execute_request_sync(method, endpoint, params)

    def list_buildings(self) -> Union[List[Building], Coroutine[Any, Any, List[Building]]]:
        """
        Retrieve a list of buildings. Returns a list if sync, or a coroutine if async.
        """
        self._log("listing_buildings", mode="auto")

        response = self._request("GET", "/v1/building")

        if self.is_async:

            async def async_result():
                try:
                    raw = await response
                    buildings = [Building(**item) for item in raw]
                    self._log("buildings_listed", mode="async", count=len(buildings))
                    return buildings
                except ValidationError as e:
                    if self.log:
                        self.log.error("validation_error", mode="async", error=str(e))
                    raise

            return async_result()

        # Modo síncrono
        try:
            buildings = [Building(**item) for item in response]
            self._log("buildings_listed", mode="sync", count=len(buildings))
            return buildings
        except ValidationError as e:
            if self.log:
                self.log.error("validation_error", mode="sync", error=str(e))
            raise

    def get_building(self, building_id: str) -> Union[Building, Coroutine[Any, Any, Building]]:
        """
        Retrieve details of a single building. Returns a Building if sync, or a coroutine if async.
        """
        self._log("getting_building", mode="auto", building_id=building_id)
        try:
            # Validate building_id upfront
            req_data = BuildingRequest(building_id=building_id)
        except ValidationError as e:
            if self.log:
                self.log.error("validation_error", building_id=building_id, error=str(e))
            raise

        endpoint = f"/v1/building/{req_data.building_id}"
        response = self._request("GET", endpoint)

        if self.is_async:

            async def async_result():
                try:
                    raw = await response
                    building = Building(**raw)
                    self._log("building_retrieved", mode="async", building_id=building_id)
                    return building
                except ValidationError as e:
                    if self.log:
                        self.log.error("validation_error", mode="async", building_id=building_id, error=str(e))
                    raise

            return async_result()

        try:
            building = Building(**response)
            self._log("building_retrieved", mode="sync", building_id=building_id)
            return building
        except ValidationError as e:
            if self.log:
                self.log.error("validation_error", mode="sync", building_id=building_id, error=str(e))
            raise

    def get_building_availability(
        self, building_id: Optional[str] = None, date: Optional[str] = None, category: Optional[str] = None
    ) -> Union[List[BuildingAvailability], Coroutine[Any, Any, List[BuildingAvailability]]]:
        """
        Retrieve availability information for a building. Returns a list if sync, or a coroutine if async.
        """
        self._log("getting_building_availability", mode="auto", building_id=building_id)
        try:
            req_data = BuildingAvailabilityRequest(building_id=building_id, date=date, category=category)
        except ValidationError as e:
            if self.log:
                self.log.error("validation_error", building_id=building_id, error=str(e))
            raise

        endpoint = f"/v1/building/availability/{req_data.building_id}"
        params = {"date": req_data.date, "category": req_data.category}
        response = self._request("GET", endpoint, params=params)

        if self.is_async:

            async def async_result():
                try:
                    raw = await response
                    availability = [BuildingAvailability(**item) for item in raw]
                    self._log(
                        "building_availability_retrieved",
                        mode="async",
                        building_id=building_id,
                        count=len(availability),
                    )
                    return availability
                except ValidationError as e:
                    if self.log:
                        self.log.error("validation_error", mode="async", building_id=building_id, error=str(e))
                    raise

            return async_result()

        try:
            availability = [BuildingAvailability(**item) for item in response]
            self._log("building_availability_retrieved", mode="sync", building_id=building_id, count=len(availability))
            return availability
        except ValidationError as e:
            if self.log:
                self.log.error("validation_error", mode="sync", building_id=building_id, error=str(e))
            raise
