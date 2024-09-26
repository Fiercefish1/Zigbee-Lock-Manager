import voluptuous as vol
from homeassistant import config_entries
from homeassistant.core import callback
from homeassistant.helpers import selector
from .const import DOMAIN, DEFAULT_SLOT_COUNT

class ZHALockUIFlowHandler(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for ZHA Lock Manager."""

    VERSION = 1
    CONNECTION_CLASS = config_entries.CONN_CLASS_LOCAL_PUSH

    async def async_step_user(self, user_input=None):
        """Handle the initial step."""
        errors = {}

        if user_input is not None:
            return self.async_create_entry(
                title="ZHA Lock Manager",
                data={
                    "lock_entity": user_input["lock_entity"],
                    "slot_count": user_input.get("slot_count", DEFAULT_SLOT_COUNT)
                }
            )

        # Define the schema for user input
        schema = vol.Schema({
            vol.Required("lock_entity"): selector.EntitySelector({
                "domain": "lock"  # Limit selection to ZHA locks
            }),
            vol.Optional("slot_count", default=DEFAULT_SLOT_COUNT): vol.Coerce(int)
        })

        return self.async_show_form(step_id="user", data_schema=schema, errors=errors)

    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        return OptionsFlowHandler(config_entry)


class OptionsFlowHandler(config_entries.OptionsFlow):
    """Handle options flow for ZHA Lock Manager."""

    def __init__(self, config_entry):
        self.config_entry = config_entry

    async def async_step_init(self, user_input=None):
        """Manage the options."""
        return self.async_show_form(
            step_id="init",
            data_schema=vol.Schema({}),
        )
