"""ADCP communication for Sony VPL ADCP."""

import socket
import logging
from .const import ADCP_COMMANDS_BY_MODEL, DEFAULT_MODEL
from homeassistant.helpers.entity import Entity

_LOGGER = logging.getLogger(__name__)


class SonyADCPClient:
    """Client for communicating with the Sony projector using ADCP protocol."""

    def __init__(
        self,
        host,
        username=None,
        password=None,
        authentication=False,
        port=53484,
        model=DEFAULT_MODEL,
    ):
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.authentication = authentication
        self.model = model
        self.socket = None

    def connect(self):
        """Establish a connection to the projector."""
        if self.socket:
            _LOGGER.warning("Socket already connected.")
            return
        try:
            self.socket = socket.create_connection((self.host, self.port), timeout=5)
            if self.authentication:
                auth_command = f"AUTH {self.username} {self.password}\n"
                self.socket.sendall(auth_command.encode("utf-8"))
                response = self.socket.recv(1024).decode("utf-8").strip()
                if response != "AUTH=OK":
                    raise ConnectionError("Authentication failed")
        except socket.timeout:
            _LOGGER.error("Connection timed out while connecting to projector.")
            raise
        except ConnectionError as err:
            _LOGGER.error("Connection error: %s", err)
            raise
        except Exception as err:
            _LOGGER.error("Unexpected error during connection: %s", err)
            raise

    def send_command(self, command):
        """Send a command to the projector."""
        if not self.socket:
            _LOGGER.error("Socket is not connected. Call connect() first.")
            return None
        try:
            self.socket.sendall(command.encode("utf-8"))
            return self.socket.recv(1024).decode("utf-8").strip()
        except socket.timeout:
            _LOGGER.error("Socket timeout while sending command '%s'.", command)
            return None
        except socket.error as err:
            _LOGGER.error("Socket error while sending command '%s': %s", command, err)
            return None
        except Exception as err:
            _LOGGER.error(
                "Unexpected error while sending command '%s': %s", command, err
            )
            return None

    def get_advertisement_attributes(self):
        """Retrieve projector attributes from the advertisement service."""
        try:
            self.socket.sendall("ADVP ?\n".encode("utf-8"))
            response = self.socket.recv(1024).decode("utf-8").strip()
            attributes = {}
            for line in response.split("\n"):
                if "=" in line:
                    key, value = line.split("=", 1)
                    attributes[key.strip()] = value.strip()
            return attributes
        except Exception as err:
            _LOGGER.error("Failed to retrieve advertisement attributes: %s", err)
            return {}

    def send_menu_command(self, command):
        """Send a menu command to the projector."""
        commands = ADCP_COMMANDS_BY_MODEL.get(self.model, {})
        if command not in commands:
            raise ValueError(f"Unsupported menu command: {command}")
        return self.send_command(commands[command])

    def get_settable_commands(self):
        """Retrieve all settable commands and their information."""
        try:
            self.socket.sendall("CMDS ?\n".encode("utf-8"))
            response = self.socket.recv(4096).decode("utf-8").strip()
            commands = {}
            for line in response.split("\n"):
                if "=" in line:
                    key, value = line.split("=", 1)
                    commands[key.strip()] = value.strip()
            return commands
        except Exception as err:
            _LOGGER.error("Failed to retrieve settable commands: %s", err)
            return {}

    def get_command_choices(self, command):
        """Retrieve the settable choices for a specific command."""
        try:
            self.socket.sendall(f"{command} ?\n".encode("utf-8"))
            response = self.socket.recv(1024).decode("utf-8").strip()
            choices = response.split(",")
            return [choice.strip() for choice in choices]
        except Exception as err:
            _LOGGER.error("Failed to retrieve choices for command %s: %s", command, err)
            return []

    def get_current_value(self, command):
        """Retrieve the current value of a specific command."""
        try:
            self.socket.sendall(f"{command} ?\n".encode("utf-8"))
            response = self.socket.recv(1024).decode("utf-8").strip()
            return response
        except Exception as err:
            _LOGGER.error(
                "Failed to retrieve current value for command %s: %s", command, err
            )
            return None

    def disconnect(self):
        """Close the connection to the projector."""
        if self.socket:
            try:
                self.socket.close()
                self.socket = None
            except Exception as err:
                _LOGGER.error("Error while closing socket: %s", err)
        else:
            _LOGGER.warning("Socket is already closed.")


class SonyADCPDevice(Entity):
    """Representation of a Sony projector as a Home Assistant entity."""

    def __init__(self, client: SonyADCPClient):
        self._client = client
        self._state = None
        self._attributes = {}

    @property
    def name(self):
        return f"Sony Projector ({self._client.host})"

    @property
    def state(self):
        return self._state

    @property
    def extra_state_attributes(self):
        return self._attributes

    def update(self):
        """Fetch new state data for the entity."""
        try:
            self._attributes = self._client.get_advertisement_attributes()
            self._state = self._client.get_current_value("POWER")
        except Exception as err:
            _LOGGER.error("Failed to update state: %s", err)
