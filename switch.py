"""Switch platform for Sony VPL-XW6000."""

from homeassistant.components.switch import SwitchEntity
from homeassistant.helpers.device_registry import async_get_registry
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed
import logging
from datetime import timedelta
from .adcp import SonyADCPClient

from .const import DOMAIN, ADCP_COMMANDS, ADCP_RESPONSES, DEFAULT_MODEL

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass, config_entry, async_add_entities):
    """Set up the switch platform."""
    host = config_entry.data.get("host")
    authentication = config_entry.data.get("authentication", False)
    username = config_entry.data.get("username")
    password = config_entry.data.get("password")
    attributes = config_entry.data.get("attributes", {})
    model = attributes.get("ModelName", DEFAULT_MODEL)

    # Register the device in the device registry
    device_registry = await async_get_registry(hass)
    device_registry.async_get_or_create(
        config_entry_id=config_entry.entry_id,
        identifiers={(DOMAIN, host)},
        manufacturer=attributes.get("Manufacturer", "Sony"),
        name=attributes.get("ModelName", "Sony VPL-XW6000 Projector"),
        model=model,
        sw_version=attributes.get("SoftwareVersion"),
    )

    async def async_update_data():
        """Fetch data from the projector."""
        client = SonyADCPClient(host, username, password, authentication, model=model)
        client.connect()
        status = client.get_status()
        client.disconnect()
        if not status:
            raise UpdateFailed("Failed to fetch projector status")
        return status

    coordinator = DataUpdateCoordinator(
        hass,
        _LOGGER,
        name="Sony Projector",
        update_method=async_update_data,
        update_interval=timedelta(minutes=1),
    )

    await coordinator.async_config_entry_first_refresh()

    async_add_entities([SonyProjectorPowerSwitch(coordinator, host, authentication, username, password, model)])

class SonyProjectorPowerSwitch(SwitchEntity):
    """Representation of the projector power switch."""

    def __init__(self, coordinator, host, authentication, username, password, model):
        self._coordinator = coordinator
        self._is_on = False
        self._host = host
        self._authentication = authentication
        self._username = username
        self._password = password
        self._model = model
        self._client = SonyADCPClient(host, username, password, authentication, model=model)

    @property
    def name(self):
        return "Sony Projector Power"

    @property
    def is_on(self):
        """Return the power state from the coordinator."""
        return self._coordinator.data.get("power") == "POWR=1"

    async def async_turn_on(self, **kwargs):
        """Turn the projector on."""
        self._client.connect()
        response = self._client.send_command(ADCP_COMMANDS["power_on"])
        self._client.disconnect()
        if response == ADCP_RESPONSES["power_on"]:
            self._is_on = True
            self.async_write_ha_state()

    async def async_turn_off(self, **kwargs):
        """Turn the projector off."""
        self._client.connect()
        response = self._client.send_command(ADCP_COMMANDS["power_off"])
        self._client.disconnect()
        if response == ADCP_RESPONSES["power_off"]:
            self._is_on = False
            self.async_write_ha_state()

    async def async_update(self):
        """Request an update from the coordinator."""
        await self._coordinator.async_request_refresh()

    async def send_menu_command(self, command):
        """Send a menu command to the projector."""
        self._client.connect()
        response = self._client.send_menu_command(command)
        self._client.disconnect()
        return response
