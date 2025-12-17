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
    API_VEHICLES,
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
        """Get all vehicles from LubeLogger."""
        vehicles = await self._async_request(API_VEHICLES)
        if not isinstance(vehicles, list):
            return []
        return vehicles

    async def async_get_latest_odometer(
        self, vehicle_id: int | None = None
    ) -> dict[str, Any] | None:
        """Get the latest odometer record for a vehicle."""
        endpoint = API_ODOMETER
        if vehicle_id:
            endpoint = f"{API_ODOMETER}?vehicleId={vehicle_id}"
        records = await self._async_request(endpoint)
        if not isinstance(records, list) or not records:
            return None
        # Filter by vehicle if needed, then sort by Id/Date
        filtered = [r for r in records if not vehicle_id or r.get("VehicleId") == vehicle_id]
        if not filtered:
            return None

        def sort_key(rec: dict[str, Any]) -> Any:
            return rec.get("Id") or rec.get("id") or rec.get("Date") or rec.get("date") or 0

        return sorted(filtered, key=sort_key)[-1]

    async def async_get_next_plan(
        self, vehicle_id: int | None = None
    ) -> dict[str, Any] | None:
        """Get the next upcoming plan item for a vehicle."""
        endpoint = API_PLAN
        if vehicle_id:
            endpoint = f"{API_PLAN}?vehicleId={vehicle_id}"
        records = await self._async_request(endpoint)
        if not isinstance(records, list) or not records:
            return None
        # Filter by vehicle if needed, then get the first (next) one
        filtered = [r for r in records if not vehicle_id or r.get("VehicleId") == vehicle_id]
        if not filtered:
            return None
        return filtered[0]

    async def async_get_latest_tax(
        self, vehicle_id: int | None = None
    ) -> dict[str, Any] | None:
        """Get the latest tax record for a vehicle."""
        endpoint = API_TAX
        if vehicle_id:
            endpoint = f"{API_TAX}?vehicleId={vehicle_id}"
        records = await self._async_request(endpoint)
        if not isinstance(records, list) or not records:
            return None

        filtered = [r for r in records if not vehicle_id or r.get("VehicleId") == vehicle_id]
        if not filtered:
            return None

        def sort_key(rec: dict[str, Any]) -> Any:
            return rec.get("Id") or rec.get("id") or rec.get("Date") or rec.get("date") or 0

        return sorted(filtered, key=sort_key)[-1]

    async def async_get_latest_service(
        self, vehicle_id: int | None = None
    ) -> dict[str, Any] | None:
        """Get the latest service record for a vehicle."""
        endpoint = API_SERVICE_RECORD
        if vehicle_id:
            endpoint = f"{API_SERVICE_RECORD}?vehicleId={vehicle_id}"
        records = await self._async_request(endpoint)
        if not isinstance(records, list) or not records:
            return None

        filtered = [r for r in records if not vehicle_id or r.get("VehicleId") == vehicle_id]
        if not filtered:
            return None

        def sort_key(rec: dict[str, Any]) -> Any:
            return rec.get("Id") or rec.get("id") or rec.get("Date") or rec.get("date") or 0

        return sorted(filtered, key=sort_key)[-1]

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
                if response.status == 404:
                    # Endpoint not found; log as debug and return empty result
                    _LOGGER.debug("Endpoint not found: %s", url)
                    return []
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

