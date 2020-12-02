"""Platform for sensor integration."""
import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import TEMP_CELSIUS
from homeassistant.helpers.entity import Entity
from homeassistant.helpers.typing import HomeAssistantType

from .const import DOMAIN, REGION_CODE
from .OctopusAgile.Agile import Agile
from .utils import get_region_code

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistantType, entry: ConfigEntry, async_add_devices
) -> bool:

    async_add_devices([PreviousRate(hass), CurrentRate(hass), NextRate(hass)])
    return True


# def setup_platform(hass, config, add_entities, discovery_info=None):
#     """Set up the sensor platform."""
#     add_entities([PreviousRate(hass)])
#     add_entities([CurrentRate(hass)])
#     add_entities([NextRate(hass)])

class PreviousRate(Entity):
    """Representation of a Sensor."""

    def __init__(self, hass):
        """Initialize the sensor."""
        self._state = None
        # self._hass = hass
        self._attributes = {}
        # if "region_code" not in self.config["OctopusAgile"]:
        #     _LOGGER.error("region_code must be set for OctopusAgile")
        # else:

        # region_code = hass.states.get("octopusagile.region_code").state
        region_code = get_region_code(hass)
        self.myrates = Agile(region_code)

    @property
    def name(self):
        """Return the name of the sensor."""
        return 'Octopus Agile Previous Rate'

    @property
    def state(self):
        """Return the state of the sensor."""
        return self._state

    @property
    def unit_of_measurement(self):
        """Return the unit of measurement."""
        return "p/kWh"

    @property
    def device_state_attributes(self):
        """Return the state attributes of the sensor."""
        return self._attributes

    def update(self):
        """Fetch new state data for the sensor.

        This is the only method that should fetch new data for Home Assistant.
        """
        # attributes = {}
        # attributes['mac'] = 'some data'
        # attributes['sn'] = 'some other data'
        # # attributes['date_to']
        # self._attributes = attributes
        rate = round(self.myrates.get_previous_rate(), 2)
        self._state = rate

class CurrentRate(Entity):
    """Representation of a Sensor."""

    def __init__(self, hass):
        """Initialize the sensor."""
        self._state = None
        # self._hass = hass
        self._attributes = {}
        # if "region_code" not in self.config["OctopusAgile"]:
        #     _LOGGER.error("region_code must be set for OctopusAgile")
        # else:

        # region_code = hass.states.get("octopusagile.region_code").state
        region_code = get_region_code(hass)
        self.myrates = Agile(region_code)

    @property
    def name(self):
        """Return the name of the sensor."""
        return 'Octopus Agile Current Rate'

    @property
    def state(self):
        """Return the state of the sensor."""
        return self._state

    @property
    def unit_of_measurement(self):
        """Return the unit of measurement."""
        return "p/kWh"

    @property
    def device_state_attributes(self):
        """Return the state attributes of the sensor."""
        return self._attributes

    def update(self):
        """Fetch new state data for the sensor.

        This is the only method that should fetch new data for Home Assistant.
        """
        # attributes = {}
        # attributes['mac'] = 'some data'
        # attributes['sn'] = 'some other data'
        # # attributes['date_to']
        # self._attributes = attributes
        rate = round(self.myrates.get_current_rate(), 2)
        self._state = rate

class NextRate(Entity):
    """Representation of a Sensor."""

    def __init__(self, hass):
        """Initialize the sensor."""
        self._state = None
        # self._hass = hass
        self._attributes = {}
        # if "region_code" not in self.config["OctopusAgile"]:
        #     _LOGGER.error("region_code must be set for OctopusAgile")
        # else:
        
        # region_code = hass.states.get("octopusagile.region_code").state
        region_code = get_region_code(hass)
        self.myrates = Agile(region_code)

    @property
    def name(self):
        """Return the name of the sensor."""
        return 'Octopus Agile Next Rate'

    @property
    def state(self):
        """Return the state of the sensor."""
        return self._state

    @property
    def unit_of_measurement(self):
        """Return the unit of measurement."""
        return "p/kWh"

    @property
    def device_state_attributes(self):
        """Return the state attributes of the sensor."""
        return self._attributes

    def update(self):
        """Fetch new state data for the sensor.

        This is the only method that should fetch new data for Home Assistant.
        """
        # attributes = {}
        # attributes['mac'] = 'some data'
        # attributes['sn'] = 'some other data'
        # # attributes['date_to']
        # self._attributes = attributes
        rate = round(self.myrates.get_next_rate(), 2)
        self._state = rate
