"""Config flow for mark integration."""
import logging
from typing import Any, Dict
import requests
import voluptuous as vol

from homeassistant import config_entries, exceptions

from .const import DOMAIN, REGION_CODE

_LOGGER = logging.getLogger(__name__)


@config_entries.HANDLERS.register(DOMAIN)
class OctopusAgileConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for installing the add-on through the GUI."""

    VERSION = 1
    # TODO pick one of the available connection classes in homeassistant/config_entries.py
    CONNECTION_CLASS = config_entries.CONN_CLASS_UNKNOWN

    async def async_step_user(self, user_input=None) -> Dict[str, Any]:
        """Handle the initial step."""
        _LOGGER.info("Setting up Octopus Agile integration")

        if user_input:
            return self.async_create_entry(
                title=DOMAIN,
                data={
                    REGION_CODE: user_input['region_code'].upper()
                }
            )

        region_code = None

        state_object = self.hass.states.get("octopusagile.region_code")

        if state_object:
            region_code = state_object.state

        if not region_code:
            region_code = await self.hass.async_add_executor_job(
                self._get_region_code_from_coords
            )

        if not region_code:
            # return self.async_abort(reason="location_error")
            return self.async_show_form(
                step_id="user",
                data_schema=vol.Schema(
                    {
                        vol.Required(
                            "region_code",
                        ): vol.All(str, vol.Length(min=1, max=1))
                    }
            ))

        self.hass.data[DOMAIN][REGION_CODE] = region_code
        return self.async_create_entry(title=DOMAIN, data={REGION_CODE: region_code})

    def _get_region_code_from_coords(self) -> str:

        latitude = self.hass.config.latitude
        longitude = self.hass.config.longitude
        outcode = _get_outcode_for_coords(latitude, longitude)
        if not outcode:
            _LOGGER.error("Could not fetch outcode from coordinates")
            return None

        self.hass.data[DOMAIN] = {}

        response = requests.get(
            f"https://api.octopus.energy/v1/industry/grid-supply-points/?postcode={outcode}"
        )

        response.raise_for_status()
        try:
            return response.json()["results"][0]["group_id"][-1]
        except:  # noqa: E722
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
