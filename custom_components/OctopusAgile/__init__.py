"""The octopusagile integration."""

import logging
from datetime import timedelta

from OctopusAgile import Agile

import homeassistant.util.dt as dt_util
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.event import async_track_point_in_time
from homeassistant.helpers.typing import HomeAssistantType

from .const import DOMAIN, REGION_CODE

_LOGGER = logging.getLogger(__name__)


def round_time(t):
    """Rounds to nearest half hour."""
    minute = 00
    if t.minute // 30 == 1:
        minute = 30
    return t.replace(second=0, microsecond=0, minute=minute, hour=t.hour)


async def async_setup(hass, config):
    """Set up is called when Home Assistant is loading our component."""
    first_run = True

    if DOMAIN not in config or REGION_CODE not in config[DOMAIN]:
        region_code = hass.config_entries.async_entries(DOMAIN)[0].data["region_code"]
    else:
        region_code = config[DOMAIN][REGION_CODE]

    _LOGGER.info("Region code loaded: " + region_code)

    agile = Agile(area_code=region_code)
    rates = await hass.async_add_executor_job(agile.get_new_rates)
    new_rates = rates["date_rates"]
    hass.states.async_set("octopusagile.rates", "", new_rates)

    def handle_half_hour_timer(call):
        """Update the next days rates."""
        new_rates = agile.get_new_rates()["date_rates"]

        hass.states.async_set("octopusagile.rates", "", new_rates)

    async def async_half_hour_timer(nowtime):
        roundedtime = agile.round_time(nowtime)
        nexttime = roundedtime + timedelta(minutes=30)
        hass.states.async_set(
            "octopusagile.half_hour_timer_nextupdate",
            nexttime.strftime("%Y-%m-%dT%H:%M:%SZ"),
        )

        try:
            if first_run is False:
                handle_half_hour_timer(None)
                hass.states.async_set(
                    "octopusagile.half_hour_timer_lastupdate",
                    nowtime.strftime("%Y-%m-%dT%H:%M:%SZ"),
                )
        except Exception as e:
            _LOGGER.error(e)

        # Setup timer to run again in 30
        async_track_point_in_time(hass, async_half_hour_timer, nexttime)

    hass.services.async_register(DOMAIN, "half_hour", handle_half_hour_timer)
    await async_half_hour_timer(dt_util.utcnow())
    first_run = False

    # Return boolean to indicate that initialization was successfully.
    return True


async def async_setup_entry(hass: HomeAssistantType, entry: ConfigEntry) -> bool:
    """Setup entry and return boolean to indicate that initialization was successful."""
    hass.async_add_job(hass.config_entries.async_forward_entry_setup(entry, "sensor"))

    _LOGGER.debug("Octopus integration entry setup complete")
    return True
