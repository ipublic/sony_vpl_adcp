"""Media Player platform for Sony VPL-XW6000."""

from homeassistant.components.media_player import MediaPlayerEntity
from homeassistant.components.media_player.const import (
    MediaPlayerDeviceClass,
    MediaPlayerEntityFeature,
)
from homeassistant.const import STATE_OFF, STATE_ON
from homeassistant.exceptions import PlatformNotReady
import logging
from .adcp import SonyADCPClient
from .const import DEFAULT_MODEL

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass, config_entry, async_add_entities):
    """Set up the media player platform."""
    host = config_entry.data.get("host")
    authentication = config_entry.data.get("authentication", False)
    username = config_entry.data.get("username")
    password = config_entry.data.get("password")

    # Connect to the projector and retrieve attributes
    client = SonyADCPClient(host, username, password, authentication)
    try:
        client.connect()
        attributes = client.get_advertisement_attributes()
    except Exception as e:
        _LOGGER.error("Failed to connect to Sony projector: %s", e)
        raise PlatformNotReady from e
    finally:
        client.disconnect()

    # Determine the model from the advertisement attributes
    model = attributes.get("ModelName", DEFAULT_MODEL)

    async_add_entities(
        [
            SonyProjectorMediaPlayer(
                host, authentication, username, password, model, attributes
            )
        ]
    )


class SonyProjectorMediaPlayer(MediaPlayerEntity):
    """Representation of the Sony VPL-XW6000 as a media player."""

    def __init__(self, host, authentication, username, password, model, attributes):
        self._host = host
        self._authentication = authentication
        self._username = username
        self._password = password
        self._model = model
        self._attributes = attributes
        self._client = SonyADCPClient(
            host, username, password, authentication, model=model
        )
        self._is_on = False
        self._input_source = None
        self._available = True  # Track availability

    @property
    def name(self):
        """Return the name of the device."""
        return self._attributes.get("ModelName", "Sony Projector")

    @property
    def state(self):
        """Return the state of the device."""
        return STATE_ON if self._is_on else STATE_OFF

    @property
    def device_class(self):
        """Return the device class of the media player."""
        return MediaPlayerDeviceClass.TV

    @property
    def supported_features(self):
        """Return the features supported by the media player."""
        return (
            MediaPlayerEntityFeature.TURN_ON
            | MediaPlayerEntityFeature.TURN_OFF
            | MediaPlayerEntityFeature.SELECT_SOURCE
            | MediaPlayerEntityFeature.NAVIGATE
        )

    @property
    def source_list(self):
        """Return the list of available input sources."""
        return ["HDMI1", "HDMI2"]

    @property
    def media_title(self):
        """Return the current input source."""
        return self._input_source

    @property
    def available(self):
        """Return if the device is available."""
        return self._available

    @property
    def device_info(self):
        """Return device information for the device registry."""
        return {
            "identifiers": {(self._host, self._model)},
            "name": self.name,
            "manufacturer": "Sony",
            "model": self._model,
        }

    async def async_update(self):
        """Fetch the latest state from the projector."""
        try:
            self._client.connect()
            power_state = self._client.get_power_state()
            self._is_on = power_state == "on"
            self._available = True
        except Exception as e:
            _LOGGER.warning("Failed to update state: %s", e)
            self._available = False
        finally:
            self._client.disconnect()

    async def async_turn_on(self):
        """Turn the projector on."""
        try:
            self._client.connect()
            self._client.send_command("POWR 1\n")
            self._is_on = True
        except Exception as e:
            _LOGGER.error("Failed to turn on projector: %s", e)
        finally:
            self._client.disconnect()
        self.async_write_ha_state()

    async def async_turn_off(self):
        """Turn the projector off."""
        try:
            self._client.connect()
            self._client.send_command("POWR 0\n")
            self._is_on = False
        except Exception as e:
            _LOGGER.error("Failed to turn off projector: %s", e)
        finally:
            self._client.disconnect()
        self.async_write_ha_state()

    async def async_select_source(self, source):
        """Select the input source."""
        self._client.connect()
        if source == "HDMI1":
            self._client.send_command("INPT 11\n")
        elif source == "HDMI2":
            self._client.send_command("INPT 12\n")
        self._client.disconnect()
        self._input_source = source
        self.async_write_ha_state()

    async def async_media_next_track(self):
        """Navigate to the next menu item."""
        await self._send_menu_command("menu_down")

    async def async_media_previous_track(self):
        """Navigate to the previous menu item."""
        await self._send_menu_command("menu_up")

    async def async_media_play(self):
        """Select the current menu item."""
        await self._send_menu_command("menu_enter")

    async def async_media_stop(self):
        """Go back in the menu."""
        await self._send_menu_command("menu_back")

    async def _send_menu_command(self, command):
        """Send a menu command to the projector."""
        self._client.connect()
        self._client.send_menu_command(command)
        self._client.disconnect()

    async def async_will_remove_from_hass(self):
        """Cleanup resources when the entity is removed."""
        self._client.disconnect()
