"""Client for interacting with LubeLogger API."""
from __future__ import annotations

import logging
from typing import Any

import aiohttp

from .const import (
    API_ODOMETER,
    API_PLAN,
    API_ROOT,
    API_SERVICE_RECORD,
    API_TAX,
)

_LOGGER = logging.getLogger(__name__)


class LubeLoggerClient:
    """Client for LubeLogger API."""

    def __init__(
        self,
        url: str,
        username: str,
        password: str,
        session: aiohttp.ClientSession | None = None,
    ) -> None:
        """Initialize the client."""
        self._url = url.rstrip("/")
        self._username = username
        self._password = password
        self._session = session
        self._auth = aiohttp.BasicAuth(username, password)

    async def async_get_vehicles(self) -> list[dict[str, Any]]:
        """Compatibility method - currently unused."""
        await self._async_request(API_ROOT)
        return []

    async def async_get_latest_odometer(self) -> dict[str, Any] | None:
        """Get the latest odometer record."""
        records = await self._async_request(API_ODOMETER)
        if not isinstance(records, list) or not records:
            return None
        # Assume records contain either an Id or Date field; pick the last one
        # This is a best-effort heuristic and may be refined based on real data.
        def sort_key(rec: dict[str, Any]) -> Any:
            return rec.get("Id") or rec.get("id") or rec.get("Date") or rec.get("date") or 0

        return sorted(records, key=sort_key)[-1]

    async def async_get_next_plan(self) -> dict[str, Any] | None:
        """Get the next upcoming plan item."""
        records = await self._async_request(API_PLAN)
        if not isinstance(records, list) or not records:
            return None
        return records[0]

    async def async_get_latest_tax(self) -> dict[str, Any] | None:
        """Get the latest tax record."""
        records = await self._async_request(API_TAX)
        if not isinstance(records, list) or not records:
            return None
        return records[-1]

    async def async_get_latest_service(self) -> dict[str, Any] | None:
        """Get the latest service record."""
        records = await self._async_request(API_SERVICE_RECORD)
        if not isinstance(records, list) or not records:
            return None
        return records[-1]

    async def _async_request(
        self, endpoint: str, method: str = "GET", **kwargs: Any
    ) -> Any:
        """Make an async request to the LubeLogger API."""
        url = f"{self._url}{endpoint}"
        session = self._session or aiohttp.ClientSession()

        try:
            async with session.request(
                method,
                url,
                auth=self._auth,
                timeout=aiohttp.ClientTimeout(total=10),
                **kwargs,
            ) as response:
                response.raise_for_status()
                if response.content_type == "application/json":
                    return await response.json()
                return await response.text()
        except aiohttp.ClientError as err:
            _LOGGER.error("Error communicating with LubeLogger API: %s", err)
            raise
        finally:
            if not self._session:
                await session.close()

