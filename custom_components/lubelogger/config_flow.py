"""Config flow for LubeLogger integration."""
from __future__ import annotations

import logging
from typing import Any

import aiohttp
import voluptuous as vol

from homeassistant import config_entries
from homeassistant.const import CONF_PASSWORD, CONF_URL, CONF_USERNAME
from homeassistant.core import HomeAssistant
from homeassistant.data_entry_flow import FlowResult
from homeassistant.exceptions import HomeAssistantError

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

STEP_USER_DATA_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_URL): str,
        vol.Required(CONF_USERNAME): str,
        vol.Required(CONF_PASSWORD): str,
    }
)


async def validate_input(hass: HomeAssistant, data: dict[str, Any]) -> dict[str, Any]:
    """Validate the user input allows us to connect."""
    url = data[CONF_URL].rstrip("/")
    username = data[CONF_USERNAME]
    password = data[CONF_PASSWORD]

    # Ensure URL has protocol
    if not url.startswith(("http://", "https://")):
        url = f"http://{url}"

    async with aiohttp.ClientSession() as session:
        try:
            # Try to authenticate and get vehicles list
            # Try multiple possible endpoints
            endpoints_to_try = [
                "/api/Vehicle/GetAllVehicles",
                "/api/Vehicle",
                "/api/vehicles",
                "/Vehicle/GetAllVehicles",
            ]
            
            last_error = None
            for endpoint in endpoints_to_try:
                try:
                    _LOGGER.debug("Trying endpoint: %s%s", url, endpoint)
                    async with session.get(
                        f"{url}{endpoint}",
                        auth=aiohttp.BasicAuth(username, password),
                        timeout=aiohttp.ClientTimeout(total=10),
                        ssl=False,  # Allow self-signed certificates
                    ) as response:
                        _LOGGER.debug("Response status: %s for %s", response.status, endpoint)
                        if response.status == 401:
                            raise InvalidAuth
                        if response.status == 200:
                            # Success! Try to parse response
                            try:
                                data = await response.json()
                                _LOGGER.debug("Successfully connected to LubeLogger")
                                return {"title": f"LubeLogger ({url})"}
                            except Exception:
                                # Even if JSON parsing fails, 200 means we connected
                                _LOGGER.debug("Connected but response not JSON")
                                return {"title": f"LubeLogger ({url})"}
                        elif response.status == 404:
                            # Endpoint not found, try next one
                            continue
                        elif response.status >= 400:
                            last_error = f"HTTP {response.status}"
                            continue
                except aiohttp.ClientConnectorError as err:
                    _LOGGER.debug("Connection error for %s: %s", endpoint, err)
                    last_error = str(err)
                    continue
                except aiohttp.ClientError as err:
                    _LOGGER.debug("Client error for %s: %s", endpoint, err)
                    last_error = str(err)
                    continue
            
            # If we get here, none of the endpoints worked
            if last_error:
                _LOGGER.error("Failed to connect to LubeLogger: %s", last_error)
                raise CannotConnect(f"Unable to connect: {last_error}")
            else:
                raise CannotConnect("Unable to connect: No valid endpoint found")
                
        except InvalidAuth:
            raise
        except CannotConnect:
            raise
        except Exception as err:
            _LOGGER.exception("Unexpected error connecting to LubeLogger: %s", err)
            raise CannotConnect(f"Connection error: {str(err)}") from err


class ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for LubeLogger."""

    VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle the initial step."""
        if user_input is None:
            return self.async_show_form(
                step_id="user", data_schema=STEP_USER_DATA_SCHEMA
            )

        # Check if this instance is already configured
        await self.async_set_unique_id(user_input[CONF_URL])
        self._abort_if_unique_id_configured()

        errors = {}

        try:
            info = await validate_input(self.hass, user_input)
        except CannotConnect:
            errors["base"] = "cannot_connect"
        except InvalidAuth:
            errors["base"] = "invalid_auth"
        except Exception:  # pylint: disable=broad-except
            _LOGGER.exception("Unexpected exception")
            errors["base"] = "unknown"
        else:
            return self.async_create_entry(title=info["title"], data=user_input)

        return self.async_show_form(
            step_id="user", data_schema=STEP_USER_DATA_SCHEMA, errors=errors
        )


class CannotConnect(HomeAssistantError):
    """Error to indicate we cannot connect."""
    
    def __init__(self, message: str = "Unable to connect to LubeLogger") -> None:
        """Initialize the error."""
        super().__init__(message)
        self.message = message


class InvalidAuth(HomeAssistantError):
    """Error to indicate there is invalid auth."""

