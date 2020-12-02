"""Config flow for mark integration."""
import logging
import requests

from typing import Any, Dict

import voluptuous as vol

from homeassistant import config_entries, core, exceptions

from .const import DOMAIN, REGION_CODE

_LOGGER = logging.getLogger(__name__)

# TODO adjust the data schema to the data that you need
DATA_SCHEMA = vol.Schema({"host": str, "username": str, "password": str})

_LOGGER.warning("Starting OctopusAgile config flow")

# TODO: Work out if this class is used
class PlaceholderHub:
    """Placeholder class to make tests pass.

    TODO Remove this placeholder class and replace with things from your PyPI package.
    """

    def __init__(self, host):
        """Initialize."""
        self.host = host

    async def authenticate(self, username, password) -> bool:
        """Test if we can authenticate with the host."""
        return True


async def validate_input(hass: core.HomeAssistant, data):
    """Validate the user input allows us to connect.

    Data has the keys from DATA_SCHEMA with values provided by the user.
    """
    # TODO validate the data can be used to set up a connection.

    # If your PyPI package is not built with async, pass your methods
    # to the executor:
    # await hass.async_add_executor_job(
    #     your_validate_func, data["username"], data["password"]
    # )

    hub = PlaceholderHub(data["host"])

    if not await hub.authenticate(data["username"], data["password"]):
        raise InvalidAuth

    # If you cannot connect:
    # throw CannotConnect
    # If the authentication is wrong:
    # InvalidAuth

    # Return info that you want to store in the config entry.
    return {"title": "Name of the device"}

@config_entries.HANDLERS.register(DOMAIN)
class OctopusAgileConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for mark."""

    _LOGGER.warning("Starting OctopusAgile config flow Class")

    VERSION = 1
    # TODO pick one of the available connection classes in homeassistant/config_entries.py
    CONNECTION_CLASS = config_entries.CONN_CLASS_UNKNOWN

    async def async_step_user(self, user_input=None) -> Dict[str, Any]:
        """Handle the initial step."""
        _LOGGER.warning("Setting up Octopus Agile integration")

        region_code = None

        value = self.hass.states.get("octopusagile.region_code")

        if value:
            region_code = value.state

        if not region_code:
            region_code = self._get_region_code_from_coords()

        if not region_code:
            return self.async_abort()

        self.hass.data[DOMAIN][REGION_CODE] = region_code
        return self.async_create_entry(title=DOMAIN, data={REGION_CODE: region_code})

    def _get_region_code_from_coords(self) -> str:
        _LOGGER.info(self.hass.config.latitude)
        _LOGGER.info(self.hass.config.longitude)

        latitude = self.hass.config.latitude
        longitude = self.hass.config.longitude
        outcode = _get_outcode_for_coords(latitude, longitude)
        if not outcode:
            return None

        self.hass.data[DOMAIN] = {}

        response = requests.get(
            f"https://api.octopus.energy/v1/industry/grid-supply-points/?postcode={outcode}"
        )

        response.raise_for_status()
        try:
            return response.json()["results"][0]["group_id"][-1]
        except:
            _LOGGER.error(response.text)
            raise


class CannotConnect(exceptions.HomeAssistantError):
    """Error to indicate we cannot connect."""


class InvalidAuth(exceptions.HomeAssistantError):
    """Error to indicate there is invalid auth."""




def _get_outcode_for_coords(lat, lon) -> str:
    response = requests.get(f"https://api.postcodes.io/outcodes?lon={lon}&lat={lat}")
    response.raise_for_status()
    if bool(response.json()["result"]):
        outcode = response.json()["result"][0]["outcode"]
        return outcode
