from typing import Any, List, Dict, Optional, Union, Coroutine
from pydantic import ValidationError
from nibol.models.booking import (
    BookingCalendarResponse,
    BookingCreateRequest,
    BookingResponse,
    BookingQuery,
)


class BookingApi:
    """
    Manages booking operations (list, create, delete) both synchronously and asynchronously.
    """

    def __init__(self, client: Any):
        # We detect if the passed client is asynchronous by checking
        # for an 'arequest' attribute or name starting with 'Async'.
        self.client = client
        self.is_async = hasattr(client, "arequest") or client.__class__.__name__.startswith("Async")
        self.log = getattr(client, "logger", None)

    def _log(self, msg: str, **kwargs):
        # Helper function for optional logging
        if self.log:
            self.log.info(msg, **kwargs)

    async def _execute_request_async(
        self, method: str, endpoint: str, payload: Optional[dict] = None, params: Optional[dict] = None
    ) -> dict:
        try:
            return await self.client.request(method=method, endpoint=endpoint, json=payload, params=params)
        except Exception as e:
            if self.log:
                self.log.error("unexpected_error", mode="async", endpoint=endpoint, error=str(e))
            raise

    def _execute_request_sync(
        self, method: str, endpoint: str, payload: Optional[dict] = None, params: Optional[dict] = None
    ) -> dict:
        try:
            return self.client.request(method=method, endpoint=endpoint, json=payload, params=params)
        except Exception as e:
            if self.log:
                self.log.error("unexpected_error", mode="sync", endpoint=endpoint, error=str(e))
            raise

    def _request(self, method: str, endpoint: str, payload=None, params=None):
        """
        Dispatch to the correct sync or async request method.
        """
        if self.is_async:
            return self._execute_request_async(method, endpoint, payload, params)
        return self._execute_request_sync(method, endpoint, payload, params)

    def list_bookings(
        self,
        page: int = 0,
        limit: int = 20,
        building: Optional[str] = None,
        space: Optional[str] = None,
        category: Optional[str] = None,
        **kwargs,
    ) -> Union[BookingCalendarResponse, Coroutine]:
        """
        List bookings (sync or async, depending on the client).
        """
        self._log("listing_bookings", mode="auto", page=page, limit=limit)
        try:
            req_data = BookingQuery(page=page, limit=limit, building=building, space=space, category=category, **kwargs)
            req_params = req_data.model_dump(exclude_none=True)
            response = self._request("GET", "/v1/booking", params=req_params)
            if self.is_async:

                async def async_result():
                    raw = await response
                    return BookingCalendarResponse(**raw)

                return async_result()
            raw = response
            return BookingCalendarResponse(**raw)
        except ValidationError as e:
            if self.log:
                self.log.error("validation_error", error=str(e))
            raise

    def create_booking(
        self,
        mode: str,
        days: List[Dict[str, Any]],
        map_entity_id: str,
        conference_link: Optional[str] = None,
        attendees: Optional[List[str]] = None,
        description: Optional[str] = None,
        title: Optional[str] = None,
    ) -> Union[BookingResponse, Coroutine]:
        """
        Create a booking (sync or async, depending on the client).
        """
        self._log("creating_booking", mode="auto", booking_mode=mode, map_entity_id=map_entity_id)
        try:
            req_data = BookingCreateRequest(
                mode=mode,
                days=days,
                map_entity_id=map_entity_id,
                conference_link=conference_link,
                attendees=attendees,
                description=description,
                title=title,
            )
            req_payload = req_data.model_dump(exclude_none=True)
            response = self._request("POST", "/v1/booking", payload=req_payload)
            if self.is_async:

                async def async_result():
                    raw = await response
                    return BookingResponse(**raw)

                return async_result()
            raw = response
            return BookingResponse(**raw)
        except ValidationError as e:
            if self.log:
                self.log.error("validation_error", error=str(e))
            raise

    def delete_booking(self, booking_id: str) -> Union[None, Coroutine]:
        """
        Delete a booking (sync or async, depending on the client).
        """
        self._log("deleting_booking", mode="auto", booking_id=booking_id)
        response = self._request("DELETE", f"/v1/booking/{booking_id}")
        if self.is_async:

            async def async_result():
                await response
                return None

            return async_result()
        return None
