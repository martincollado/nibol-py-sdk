from typing import Optional
from nibol.clients.sync_client import SyncApiClient
from nibol.clients.async_client import AsyncApiClient
from nibol.apis.booking import BookingApi
from nibol.apis.building import BuildingApi
from nibol.apis.space import SpaceApi
from nibol.apis.user import UserApi


class NibolClient:
    def __init__(
        self,
        base_url: str,
        api_key: Optional[str] = None,
        user_email: Optional[str] = None,
        timeout: int = 10,
    ):
        self._client = SyncApiClient(base_url=base_url, api_key=api_key, user_email=user_email, timeout=timeout)
        self.bookings = BookingApi(self._client)
        self.buildings = BuildingApi(self._client)
        self.spaces = SpaceApi(self._client)
        self.users = UserApi(self._client)

    def __del__(self):
        if hasattr(self, "_client"):
            self._client.close()


class NibolAsyncClient:
    def __init__(
        self,
        base_url: str,
        api_key: Optional[str] = None,
        user_email: Optional[str] = None,
        timeout: int = 10,
    ):
        self._client = AsyncApiClient(base_url=base_url, api_key=api_key, user_email=user_email, timeout=timeout)
        self.bookings = BookingApi(self._client)
        self.buildings = BuildingApi(self._client)
        self.spaces = SpaceApi(self._client)
        self.users = UserApi(self._client)

    async def __del__(self):
        if hasattr(self, "_client"):
            await self._client.close()
