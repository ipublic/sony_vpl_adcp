"""Config flow for Sony VPL-XW6000 integration."""

from homeassistant import config_entries
import voluptuous as vol
import ipaddress
from .adcp import SonyADCPClient
from .const import DOMAIN


class SonyVPLXW6000ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Sony VPL-XW6000."""

    async def async_step_user(self, user_input=None):
        """Handle the initial step."""
        errors = {}

        if user_input is not None:
            # Validate the network connection and authentication
            host = user_input["host"]
            authentication = user_input.get("authentication", False)
            username = user_input.get("username")
            password = user_input.get("password")

            try:
                # Test the connection and authentication
                client = SonyADCPClient(
                    host=host,
                    username=username,
                    password=password,
                    authentication=authentication,
                )
                client.connect()
                attributes = (
                    client.get_projector_attributes()
                )  # Fetch projector attributes
                client.disconnect()

                # Store attributes in the config entry
                user_input["attributes"] = attributes
            except ConnectionError:
                errors["base"] = "connection_failed"
            except Exception:
                errors["base"] = "unknown_error"

            if not errors:
                # If validation succeeds, create the config entry
                return self.async_create_entry(title="Sony VPL-XW6000", data=user_input)

        # Show the form to collect configuration data
        return self.async_show_form(
            step_id="user",
            data_schema=self._get_data_schema(),
            errors=errors,
        )

    def _get_data_schema(self):
        """Return the data schema for the configuration form."""
        return vol.Schema(
            {
                vol.Required("host"): vol.All(str, self._validate_ip),
                vol.Optional("authentication", default=False): bool,
                vol.Optional("username"): str,
                vol.Optional("password"): str,
            }
        )

    def _validate_ip(self, value):
        """Validate the IP address."""
        try:
            ipaddress.ip_address(value)
            return value
        except ValueError:
            raise vol.Invalid("Invalid IP address")
