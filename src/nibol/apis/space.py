from typing import Any, List, Optional, Union, Coroutine
from pydantic import ValidationError
from nibol.models.space import (
    Space,
    SpaceAvailability,
    SpaceAvailabilityRequest,
    SpaceDetails,
    SpaceListRequest,
    SpaceDetailsRequest,
)


class SpaceAPI:
    """
    Manages Space operations (list, get, availability) in both sync and async modes.
    """

    def __init__(self, client: Any):
        # Detect if the client is async by checking for 'arequest' or class name.
        self.client = client
        self.is_async = hasattr(client, "arequest") or client.__class__.__name__.startswith("Async")
        self.log = getattr(client, "logger", None)

    def _log(self, message: str, **kwargs) -> None:
        if self.log:
            self.log.info(message, **kwargs)

    async def _execute_request_async(self, method: str, endpoint: str, params: Optional[dict] = None) -> Any:
        """
        Internal method to execute an async request using the client's async method.
        """
        try:
            return await self.client.request(
                method=method,
                endpoint=endpoint,
                params=params,
            )
        except Exception as e:
            if self.log:
                self.log.error("unexpected_error", mode="async", endpoint=endpoint, error=str(e))
            raise

    def _execute_request_sync(self, method: str, endpoint: str, params: Optional[dict] = None) -> Any:
        """
        Internal method to execute a sync request using the client's sync method.
        """
        try:
            return self.client.request(
                method=method,
                endpoint=endpoint,
                params=params,
            )
        except Exception as e:
            if self.log:
                self.log.error("unexpected_error", mode="sync", endpoint=endpoint, error=str(e))
            raise

    def _request(
        self, method: str, endpoint: str, params: Optional[dict] = None
    ) -> Union[Any, Coroutine[Any, Any, Any]]:
        """
        Dispatch method that calls the appropriate sync or async request method.
        Returns the raw response or a coroutine, depending on `is_async`.
        """
        if self.is_async:
            return self._execute_request_async(method, endpoint, params)
        return self._execute_request_sync(method, endpoint, params)

    def list_spaces(self, building: str) -> Union[List[Space], Coroutine[Any, Any, List[Space]]]:
        """
        Retrieve the list of spaces for a building.
        Returns a list if sync, or a coroutine if async.
        """
        self._log("listing_spaces", mode="auto", building=building)
        try:
            req_data = SpaceListRequest(building=building)
        except ValidationError as e:
            if self.log:
                self.log.error("validation_error", building=building, error=str(e))
            raise

        response = self._request("GET", "/v1/space/", params=req_data.model_dump(by_alias=True))
        if self.is_async:

            async def async_result():
                try:
                    raw = await response
                    spaces = [Space(**space) for space in raw]
                    self._log("spaces_listed", mode="async", building=building, count=len(spaces))
                    return spaces
                except ValidationError as e:
                    if self.log:
                        self.log.error("validation_error", mode="async", building=building, error=str(e))
                    raise

            return async_result()

        try:
            spaces = [Space(**space) for space in response]
            self._log("spaces_listed", mode="sync", building=building, count=len(spaces))
            return spaces
        except ValidationError as e:
            if self.log:
                self.log.error("validation_error", mode="sync", building=building, error=str(e))
            raise

    def get_space(self, space_id: str) -> Union[SpaceDetails, Coroutine[Any, Any, SpaceDetails]]:
        """
        Retrieve details of a single space.
        Returns a SpaceDetails object if sync, or a coroutine if async.
        """
        self._log("getting_space", mode="auto", space_id=space_id)
        try:
            SpaceDetailsRequest(space_id=space_id)  # Validate upfront
        except ValidationError as e:
            if self.log:
                self.log.error("validation_error", space_id=space_id, error=str(e))
            raise

        endpoint = f"/v1/space/{space_id}"
        response = self._request("GET", endpoint)
        if self.is_async:

            async def async_result():
                try:
                    raw = await response
                    details = SpaceDetails(**raw)
                    self._log("space_retrieved", mode="async", space_id=space_id)
                    return details
                except ValidationError as e:
                    if self.log:
                        self.log.error("validation_error", mode="async", space_id=space_id, error=str(e))
                    raise

            return async_result()

        try:
            details = SpaceDetails(**response)
            self._log("space_retrieved", mode="sync", space_id=space_id)
            return details
        except ValidationError as e:
            if self.log:
                self.log.error("validation_error", mode="sync", space_id=space_id, error=str(e))
            raise

    def get_space_availability(
        self, space_id: str, date: str
    ) -> Union[List[SpaceAvailability], Coroutine[Any, Any, List[SpaceAvailability]]]:
        """
        Retrieve the availability of a specific space for a given date.
        Returns a list if sync, or a coroutine if async.
        """
        self._log("getting_space_availability", mode="auto", space_id=space_id, date=date)
        try:
            req_data = SpaceAvailabilityRequest.validate_request(space_id=space_id, date=date)
        except ValidationError as e:
            if self.log:
                self.log.error("validation_error", space_id=space_id, error=str(e))
            raise

        endpoint = f"/v1/space/availability/{req_data.space_id}"
        response = self._request("GET", endpoint, params={"date": req_data.date})
        if self.is_async:

            async def async_result():
                try:
                    raw = await response
                    availability = [SpaceAvailability(**item) for item in raw]
                    self._log("space_availability_retrieved", mode="async", space_id=space_id, count=len(availability))
                    return availability
                except ValidationError as e:
                    if self.log:
                        self.log.error("validation_error", mode="async", space_id=space_id, error=str(e))
                    raise

            return async_result()

        try:
            availability = [SpaceAvailability(**item) for item in response]
            self._log("space_availability_retrieved", mode="sync", space_id=space_id, count=len(availability))
            return availability
        except ValidationError as e:
            if self.log:
                self.log.error("validation_error", mode="sync", space_id=space_id, error=str(e))
            raise

    def get_categories(self, space_id: str) -> Union[List[str], Coroutine[Any, Any, List[str]]]:
        """
        Retrieve the list of unique categories from a space's map entities.
        Returns a list if sync, or a coroutine if async.
        """
        self._log("getting_space_categories", mode="auto", space_id=space_id)

        # Llamamos a get_space, que puede ser sync o async
        space_result = self.get_space(space_id)

        if self.is_async:

            async def async_result():
                sp = await space_result  # SpaceDetails
                categories = [entity["category"] for entity in sp.map_entities]
                unique_cats = sorted(set(categories))
                self._log("space_categories_retrieved", mode="async", space_id=space_id, count=len(unique_cats))
                return unique_cats

            return async_result()

        # Modo síncrono
        sp = space_result  # SpaceDetails
        categories = [entity["category"] for entity in sp.map_entities]
        unique_cats = sorted(set(categories))
        self._log("space_categories_retrieved", mode="sync", space_id=space_id, count=len(unique_cats))
        return unique_cats
