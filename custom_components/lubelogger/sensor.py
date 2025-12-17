"""Sensor platform for LubeLogger integration."""
from __future__ import annotations

from datetime import datetime
from typing import Any

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorStateClass,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.util import dt as dt_util

from .coordinator import LubeLoggerDataUpdateCoordinator


def parse_date(date_str: str | None) -> datetime | None:
    """Parse a date string from LubeLogger API."""
    if not date_str:
        return None

    # Try ISO format first
    try:
        if date_str.endswith("Z"):
            date_str = date_str.replace("Z", "+00:00")
        return datetime.fromisoformat(date_str.replace("Z", "+00:00"))
    except (ValueError, AttributeError):
        pass

    # Try common date formats
    formats = [
        "%Y-%m-%dT%H:%M:%S",
        "%Y-%m-%dT%H:%M:%S.%f",
        "%Y-%m-%d %H:%M:%S",
        "%Y-%m-%d",
    ]

    for fmt in formats:
        try:
            return datetime.strptime(date_str, fmt)
        except (ValueError, AttributeError):
            continue

    return None


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up LubeLogger sensors from a config entry."""
    coordinator: LubeLoggerDataUpdateCoordinator = hass.data["lubelogger"][
        entry.entry_id
    ]

    sensors: list[SensorEntity] = [
        LubeLoggerLatestOdometerSensor(coordinator),
        LubeLoggerNextPlanSensor(coordinator),
        LubeLoggerLatestTaxSensor(coordinator),
        LubeLoggerLatestServiceSensor(coordinator),
    ]

    async_add_entities(sensors)


class BaseLubeLoggerSensor(CoordinatorEntity, SensorEntity):
    """Base sensor that reads a key from coordinator data."""

    def __init__(
        self,
        coordinator: LubeLoggerDataUpdateCoordinator,
        key: str,
        name: str,
        unique_id: str,
        device_class: SensorDeviceClass | None = None,
        state_class: SensorStateClass | None = None,
        unit: str | None = None,
    ) -> None:
        super().__init__(coordinator)
        self._key = key
        self._attr_name = name
        self._attr_unique_id = unique_id
        self._attr_device_class = device_class
        self._attr_state_class = state_class
        self._attr_native_unit_of_measurement = unit

    @property
    def _record(self) -> dict | None:
        data = self.coordinator.data or {}
        rec = data.get(self._key)
        return rec if isinstance(rec, dict) else None


class LubeLoggerLatestOdometerSensor(BaseLubeLoggerSensor):
    """Sensor for latest odometer value."""

    def __init__(self, coordinator: LubeLoggerDataUpdateCoordinator) -> None:
        super().__init__(
            coordinator,
            key="latest_odometer",
            name="LubeLogger Latest Odometer",
            unique_id="lubelogger_latest_odometer",
            device_class=SensorDeviceClass.DISTANCE,
            state_class=SensorStateClass.MEASUREMENT,
            unit="km",
        )

    @property
    def native_value(self) -> Any:
        rec = self._record
        if not rec:
            return None
        # Best-effort field guessing; adjust based on actual API fields.
        return (
            rec.get("Odometer")
            or rec.get("odometer")
            or rec.get("Value")
            or rec.get("value")
        )

    @property
    def extra_state_attributes(self) -> dict[str, Any] | None:
        return self._record or None


class LubeLoggerNextPlanSensor(BaseLubeLoggerSensor):
    """Sensor for next planned item from Plan endpoint."""

    def __init__(self, coordinator: LubeLoggerDataUpdateCoordinator) -> None:
        super().__init__(
            coordinator,
            key="next_plan",
            name="LubeLogger Next Plan",
            unique_id="lubelogger_next_plan",
            device_class=SensorDeviceClass.TIMESTAMP,
        )

    @property
    def native_value(self) -> datetime | None:
        rec = self._record
        if not rec:
            return None

        # Try common field names for due date
        for field in ("NextDueDate", "DueDate", "Date", "date"):
            dt = parse_date(rec.get(field))
            if dt:
                return dt
        return None

    @property
    def extra_state_attributes(self) -> dict[str, Any] | None:
        return self._record or None


class LubeLoggerLatestTaxSensor(BaseLubeLoggerSensor):
    """Sensor for latest tax record."""

    def __init__(self, coordinator: LubeLoggerDataUpdateCoordinator) -> None:
        super().__init__(
            coordinator,
            key="latest_tax",
            name="LubeLogger Latest Tax",
            unique_id="lubelogger_latest_tax",
            device_class=SensorDeviceClass.MONETARY,
            state_class=None,
            unit="USD",
        )

    @property
    def native_value(self) -> Any:
        rec = self._record
        if not rec:
            return None
        # Guess amount field
        return (
            rec.get("Amount")
            or rec.get("amount")
            or rec.get("Cost")
            or rec.get("cost")
        )

    @property
    def extra_state_attributes(self) -> dict[str, Any] | None:
        return self._record or None


class LubeLoggerLatestServiceSensor(BaseLubeLoggerSensor):
    """Sensor for latest service record."""

    def __init__(self, coordinator: LubeLoggerDataUpdateCoordinator) -> None:
        super().__init__(
            coordinator,
            key="latest_service",
            name="LubeLogger Latest Service",
            unique_id="lubelogger_latest_service",
            device_class=SensorDeviceClass.TIMESTAMP,
        )

    @property
    def native_value(self) -> datetime | None:
        rec = self._record
        if not rec:
            return None

        for field in ("ServiceDate", "Date", "date"):
            dt = parse_date(rec.get(field))
            if dt:
                return dt
        return None

    @property
    def extra_state_attributes(self) -> dict[str, Any] | None:
        return self._record or None
