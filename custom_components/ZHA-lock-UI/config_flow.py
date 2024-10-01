import voluptuous as vol
from homeassistant import config_entries
from .const import DOMAIN
import logging

_LOGGER = logging.getLogger(__name__)

class LockCodeFlowHandler(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle the configuration flow for Zigbee Lock Manager."""

    VERSION = 1

    async def async_step_user(self, user_input=None):
        """Handle the initial step."""
        errors = {}

        # Fetch available lock entities
        lock_entities = [entity.entity_id for entity in self.hass.states.async_all("lock")]

        # Handle the case where no lock entities are available
        if not lock_entities:
            errors["base"] = "no_locks"
            _LOGGER.warning("No locks found during config flow")
            return self.async_show_form(
                step_id="user",
                errors=errors,
                description_placeholders={"error": "No locks found in your Home Assistant instance."},
            )

        if user_input is not None:
            _LOGGER.debug(f"User input: {user_input}")
            return self.async_create_entry(title="Zigbee Lock Manager", data=user_input)

        # Define the form schema
        schema = vol.Schema({
            vol.Required("slot_count", default=1): vol.Coerce(int),
            vol.Required("lock_name", default=lock_entities[0]): vol.In(lock_entities),
        })

        return self.async_show_form(step_id="user", data_schema=schema, errors=errors)
