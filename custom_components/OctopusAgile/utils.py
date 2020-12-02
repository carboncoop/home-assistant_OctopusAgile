"""Small utility functions"""

from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.typing import HomeAssistantType

from .const import DOMAIN, REGION_CODE

def get_region_code(hass: HomeAssistantType) -> str:
    """Returns the Octopus region code"""

    # TODO: find a way to load from config file if possible
    # if DOMAIN not in hass.config.as_dict() or REGION_CODE not in hass.config.as_dict()[DOMAIN]:
    #     region_code = hass.config_entries.async_entries(DOMAIN)[0].data[REGION_CODE]
    # else:
    #     region_code = hass.config[DOMAIN][REGION_CODE]

    region_code = hass.config_entries.async_entries(DOMAIN)[0].data[REGION_CODE]

    return region_code
