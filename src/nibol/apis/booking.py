from typing import Dict, Any
from nibol.models.booking import (
    BookingQuery,
    BookingCreateRequest,
    BookingCalendarResponse,
)


class BookingApi:
    def __init__(self, client: Any):
        self.client = client

    async def get_bookings(self, params: BookingQuery) -> BookingCalendarResponse:
        """Retrieve bookings."""
        response = await self.client.request(
            method="GET",
            endpoint="/v1/booking/calendar",
            params=params.dict(exclude_none=True),
        )
        return BookingCalendarResponse(**response)

    async def create_booking(self, payload: BookingCreateRequest) -> Dict[str, Any]:
        """Create a new booking."""
        return await self.client.request(method="POST", endpoint="/v1/booking/", json=payload.dict())
