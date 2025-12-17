"""Data update coordinator for LubeLogger."""
from __future__ import annotations

import logging
from datetime import timedelta

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .client import LubeLoggerClient
from .const import (
    CONF_PASSWORD,
    CONF_URL,
    CONF_USERNAME,
    DEFAULT_UPDATE_INTERVAL,
    DOMAIN,
)

_LOGGER = logging.getLogger(__name__)


class LubeLoggerDataUpdateCoordinator(DataUpdateCoordinator):
    """Class to manage fetching LubeLogger data."""

    def __init__(self, hass: HomeAssistant, entry: ConfigEntry) -> None:
        """Initialize the coordinator."""
        self.entry = entry
        self.client = LubeLoggerClient(
            url=entry.data[CONF_URL],
            username=entry.data[CONF_USERNAME],
            password=entry.data[CONF_PASSWORD],
        )

        update_interval = timedelta(
            seconds=entry.options.get("update_interval", DEFAULT_UPDATE_INTERVAL)
        )

        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=update_interval,
        )

    async def _async_update_data(self) -> dict:
        """Fetch data from LubeLogger."""
        data: dict = {}

        # Latest odometer
        try:
            data["latest_odometer"] = await self.client.async_get_latest_odometer()
        except Exception as err:  # pragma: no cover - defensive
            _LOGGER.warning("Error fetching latest odometer: %s", err)
            data["latest_odometer"] = None

        # Next planned item
        try:
            data["next_plan"] = await self.client.async_get_next_plan()
        except Exception as err:  # pragma: no cover - defensive
            _LOGGER.warning("Error fetching next plan item: %s", err)
            data["next_plan"] = None

        # Latest tax
        try:
            data["latest_tax"] = await self.client.async_get_latest_tax()
        except Exception as err:  # pragma: no cover - defensive
            _LOGGER.warning("Error fetching latest tax record: %s", err)
            data["latest_tax"] = None

        # Latest service record
        try:
            data["latest_service"] = await self.client.async_get_latest_service()
        except Exception as err:  # pragma: no cover - defensive
            _LOGGER.warning("Error fetching latest service record: %s", err)
            data["latest_service"] = None

        return data

