"""Sony VPL home theater laser projector integration."""

from homeassistant.components.sensor import SensorEntity
from homeassistant.exceptions import PlatformNotReady
from homeassistant.helpers.entity import EntityCategory
from homeassistant.helpers import persistent_notification
from .adcp import SonyADCPClient
from .const import DEFAULT_MODEL


async def async_setup_entry(hass, config_entry, async_add_entities):
    """Set up the sensor platform."""
    host = config_entry.data.get("host")
    authentication = config_entry.data.get("authentication", False)
    username = config_entry.data.get("username")
    password = config_entry.data.get("password")
    model = config_entry.data.get("model", DEFAULT_MODEL)

    client = SonyADCPClient(host, username, password, authentication, model=model)
    try:
        await client.async_connect()
        commands = await client.async_get_settable_commands()
        await client.async_disconnect()
    except ConnectionError as e:
        raise PlatformNotReady(f"Connection error: {e}")
    except Exception as e:
        raise PlatformNotReady(f"Unexpected error: {e}")

    # Create sensor entities for each command
    sensors = [
        SonyProjectorSensor(
            hass,
            client,
            host,
            authentication,
            username,
            password,
            model,
            command,
            description,
        )
        for command, description in commands.items()
    ]

    async_add_entities(sensors)


class SonyProjectorSensor(SensorEntity):
    """Representation of a Sony projector sensor."""

    def __init__(
        self,
        hass,
        client,
        host,
        authentication,
        username,
        password,
        model,
        command,
        description,
    ):
        self.hass = hass
        self._client = client
        self._host = host
        self._authentication = authentication
        self._username = username
        self._password = password
        self._model = model
        self._command = command
        self._description = description
        self._state = None

    @property
    def name(self):
        """Return the name of the sensor."""
        return f"Projector {self._description}"

    @property
    def unique_id(self):
        """Return a unique ID for the sensor."""
        return f"{self._host}_{self._command}"

    @property
    def state(self):
        """Return the state of the sensor."""
        return self._state

    @property
    def entity_category(self):
        """Return the entity category (e.g., diagnostic)."""
        return EntityCategory.DIAGNOSTIC

    async def async_update(self):
        """Fetch the latest state of the sensor."""
        try:
            await self._client.async_connect()
            self._state = await self._client.async_get_current_value(self._command)
            await self._client.async_disconnect()
        except ConnectionError as e:
            self._state = None
            self.hass.logger.error(f"Connection error for sensor {self.name}: {e}")
            persistent_notification.async_create(
                self.hass,
                f"Failed to update sensor {self.name}. Connection error: {e}",
                title="Sony Projector Integration",
            )
        except Exception as e:
            self._state = None
            self.hass.logger.error(f"Unexpected error for sensor {self.name}: {e}")
            persistent_notification.async_create(
                self.hass,
                f"Failed to update sensor {self.name}. Unexpected error: {e}",
                title="Sony Projector Integration",
            )
