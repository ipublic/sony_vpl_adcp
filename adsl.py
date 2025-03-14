"""ADSL communication for Sony VPL-XW6000."""

import socket
import logging

_LOGGER = logging.getLogger(__name__)


class SonyADSLClient:
    """Client for communicating with the Sony projector using ADSL protocol."""

    def __init__(self, host: str, port: int = 53484):
        """Initialize the ADSL client."""
        self.host = host
        self.port = port
        self.socket = None

    def connect(self):
        """Establish a connection to the projector."""
        try:
            self.socket = socket.create_connection((self.host, self.port), timeout=5)
            _LOGGER.info("Connected to Sony projector at %s:%s", self.host, self.port)
        except (socket.timeout, socket.error) as err:
            _LOGGER.error("Failed to connect to projector: %s", err)
            self.socket = None

    def send_command(self, command: str) -> str:
        """Send a command to the projector and return the response."""
        if not self.socket:
            _LOGGER.error("No connection to projector. Call connect() first.")
            return None

        try:
            _LOGGER.debug("Sending command: %s", command.strip())
            self.socket.sendall(command.encode("utf-8"))
            response = self.socket.recv(1024).decode("utf-8").strip()
            _LOGGER.debug("Received response: %s", response)
            return response
        except (socket.error, socket.timeout) as err:
            _LOGGER.error("Error communicating with projector: %s", err)
            return None

    def disconnect(self):
        """Close the connection to the projector."""
        if self.socket:
            try:
                self.socket.close()
                _LOGGER.info("Disconnected from Sony projector.")
            except socket.error as err:
                _LOGGER.error("Error closing connection: %s", err)
            finally:
                self.socket = None
