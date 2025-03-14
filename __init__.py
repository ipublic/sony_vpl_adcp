"""Sony VPL home theater laser projector integration."""

import logging  # Added logging import
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed
from datetime import timedelta
from .adcp import SonyADCPClient  # Import SonyADCPClient

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)  # Define logger


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up the Sony VPL-XW6000 integration from a config entry."""
    hass.data.setdefault(DOMAIN, {})
    coordinator = DataUpdateCoordinator(
        hass,
        _LOGGER,
        name="sony_vpl_adcp",
        update_method=lambda: fetch_projector_status(entry.data),
        update_interval=timedelta(seconds=30),
    )
    await coordinator.async_config_entry_first_refresh()
    hass.data[DOMAIN][entry.entry_id] = coordinator
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    coordinator = hass.data[DOMAIN].pop(entry.entry_id, None)
    if coordinator:
        await coordinator.async_close()  # Ensure proper cleanup
    return True


async def fetch_projector_status(config):
    """Fetch the projector's status."""
    try:
        client = SonyADCPClient(
            host=config["host"],
            username=config.get("username"),
            password=config.get("password"),
            authentication=config.get("authentication", False),
        )
        await client.async_connect()  # Use async method if supported
        status = await client.async_get_advertisement_attributes()  # Use async method
        await client.async_disconnect()  # Use async method
        return status
    except ConnectionError as conn_err:
        _LOGGER.error("Connection error: %s", conn_err)
        raise UpdateFailed(f"Connection error: {conn_err}")
    except Exception as err:
        _LOGGER.exception("Unexpected error: %s", err)
        raise UpdateFailed(f"Error fetching projector status: {err}")
