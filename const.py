"""Constants for the Sony VPL ADCP integration."""

DOMAIN = "sony_vpl_adcp"

# ADCP Protocol Constants
ADCP_PORT = 53484  # Default port for ADCP communication

# Home Assistant Service Constants
SERVICE_POWER_ON = "power_on"
SERVICE_POWER_OFF = "power_off"
SERVICE_GET_POWER_STATUS = "get_power_status"
SERVICE_GET_INPUT_STATUS = "get_input_status"
SERVICE_SET_INPUT_HDMI1 = "set_input_hdmi1"
SERVICE_SET_INPUT_HDMI2 = "set_input_hdmi2"

# ADCP Commands by Model
# Ensure all models have consistent commands
ADCP_COMMANDS_BY_MODEL = {
    "VPL-XW7000": {
        "menu_up": "MENU UP\n",
        "menu_down": "MENU DOWN\n",
        "menu_left": "MENU LEFT\n",
        "menu_right": "MENU RIGHT\n",
        "menu_enter": "MENU ENTER\n",
        "menu_back": "MENU BACK\n",
        "menu_open": "MENU 1\n",
        "menu_close": "MENU 0\n",
        "menu_info": "MENU INFO\n",  # Added for consistency
    },
    "VPL-XW6000": {
        "menu_up": "MENU UP\n",
        "menu_down": "MENU DOWN\n",
        "menu_left": "MENU LEFT\n",
        "menu_right": "MENU RIGHT\n",
        "menu_enter": "MENU ENTER\n",
        "menu_back": "MENU BACK\n",
        "menu_info": "MENU INFO\n",  # Added for consistency
        "menu_open": "MENU 1\n",     # Added for consistency
        "menu_close": "MENU 0\n",    # Added for consistency
    },
    "VPL-XW5000": {
        "menu_up": "MENU UP\n",
        "menu_down": "MENU DOWN\n",
        "menu_left": "MENU LEFT\n",
        "menu_right": "MENU RIGHT\n",
        "menu_enter": "MENU ENTER\n",
        "menu_back": "MENU BACK\n",
        "menu_info": "MENU INFO\n",
    },
}

# Default Model
DEFAULT_MODEL = "VPL-XW6000"

# ADCP_COMMANDS: General commands applicable to all models
ADCP_COMMANDS = {
    "power_on": "POWR 1\n",
    "power_off": "POWR 0\n",
    "get_power_status": "POWR ?\n",
    "get_input_status": "INPT ?\n",
    "set_input_hdmi1": "INPT 11\n",
    "set_input_hdmi2": "INPT 12\n",
}

# ADCP_RESPONSES: Expected responses for specific commands
ADCP_RESPONSES = {
    "power_on": "POWR=1",
    "power_off": "POWR=0",
}
