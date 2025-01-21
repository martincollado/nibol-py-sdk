from typing import Optional, Union
from nibol.clients.sync_client import SyncApiClient
from nibol.clients.async_client import AsyncApiClient
from nibol.apis.booking import BookingAPI
from nibol.apis.building import BuildingAPI
from nibol.apis.space import SpaceAPI
from nibol.apis.user import UserAPI
from nibol.logger import LoggerType, LogLevel, setup_logger

__all__ = ["SyncApiClient", "AsyncApiClient", "NibolClient", "NibolAsyncClient"]


class NibolClient:
    def __init__(
        self,
        api_key: str,
        user_email: str,
        base_url: str = "https://api.nibol.com/public",
        logger_type: Union[LoggerType, str] = LoggerType.JSON,
        log_level: LogLevel = "INFO",
        service_name: str = "nibol-client",
        project_id: Optional[str] = None,
        timeout: int = 10,
    ):
        self._client = SyncApiClient(base_url=base_url, api_key=api_key, user_email=user_email, timeout=timeout)

        # Setup logger
        self.logger = setup_logger(
            logger_type=logger_type, level=log_level, service_name=service_name, project_id=project_id
        )

        self.bookings = BookingAPI(self._client)
        self.buildings = BuildingAPI(self._client)
        self.spaces = SpaceAPI(self._client)
        self.users = UserAPI(self._client)


class NibolAsyncClient:
    def __init__(
        self,
        api_key: str,
        user_email: str,
        base_url: str = "https://api.nibol.com/public",
        logger_type: Union[LoggerType, str] = LoggerType.JSON,
        log_level: LogLevel = "INFO",
        service_name: str = "nibol-client",
        project_id: Optional[str] = None,
        timeout: int = 10,
    ):
        self._client = AsyncApiClient(base_url=base_url, api_key=api_key, user_email=user_email, timeout=timeout)

        # Setup logger
        self.logger = setup_logger(
            logger_type=logger_type, level=log_level, service_name=service_name, project_id=project_id
        )

        self.bookings = BookingAPI(self._client)
        self.buildings = BuildingAPI(self._client)
        self.spaces = SpaceAPI(self._client)
        self.users = UserAPI(self._client)

    async def close(self):
        await self._client.close()

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()
