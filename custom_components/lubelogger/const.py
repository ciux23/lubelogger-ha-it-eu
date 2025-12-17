"""Constants for the LubeLogger integration."""
from typing import Final

DOMAIN: Final = "lubelogger"

CONF_URL: Final = "url"
CONF_USERNAME: Final = "username"
CONF_PASSWORD: Final = "password"
CONF_UPDATE_INTERVAL: Final = "update_interval"

DEFAULT_UPDATE_INTERVAL: Final = 300  # 5 minutes

# API endpoints
# The LubeLogger API is rooted at /api and exposes multiple resources.
# See https://docs.lubelogger.com/Advanced/API for details.
API_ROOT: Final = "/api"

# Vehicle-scoped endpoints (all vehicles)
API_ODOMETER: Final = "/api/vehicle/odometerrecords/all"
API_PLAN: Final = "/api/vehicle/planrecords/all"
API_TAX: Final = "/api/vehicle/taxrecords/all"
API_SERVICE_RECORD: Final = "/api/vehicle/servicerecords/all"


