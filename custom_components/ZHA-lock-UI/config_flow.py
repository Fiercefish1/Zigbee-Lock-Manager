from homeassistant import config_entries
from .const import DOMAIN

class LockCodeFlowHandler(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle the configuration flow for Zigbee Lock Manager."""

    VERSION = 1

    async def async_step_user(self, user_input=None):
        """Handle the initial step."""
        errors = {}

        if user_input is not None:
            # Store user input (number of slots) and create the config entry
            return self.async_create_entry(title="Zigbee Lock Manager", data=user_input)

        # Define the form schema
        schema = vol.Schema({
            vol.Required("slot_count", default=1): vol.Coerce(int)
        })

        return self.async_show_form(step_id="user", data_schema=schema, errors=errors)
