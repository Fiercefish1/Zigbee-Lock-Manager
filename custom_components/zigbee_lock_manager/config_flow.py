import voluptuous as vol
from homeassistant import config_entries
from .const import DOMAIN
import logging

_LOGGER = logging.getLogger(__name__)

class LockCodeFlowHandler(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle the configuration flow for Zigbee Lock Manager."""

    VERSION = 1.0

    async def async_step_user(self, user_input=None):
        """Handle the initial step."""
        errors = {}

        # Fetch available lock entities (assume they are in the format lock.some_lock_name)
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
            # Extract only the part after "lock." from the lock entity ID
            full_lock_entity_id = user_input["lock_name"]
            lock_name = full_lock_entity_id.split("lock.")[1]

            # Store the processed lock_name instead of the full entity ID
            user_input["lock_name"] = lock_name

            _LOGGER.debug(f"User input: {user_input}")
            
            # Automatically use the lock_name as the title for the integration entry
            return self.async_create_entry(title=f"Zigbee Lock Manager - {lock_name}", data=user_input)

        # Define the form schema
        schema = vol.Schema({
            vol.Required("slot_count", default=1): vol.Coerce(int),
            vol.Required("lock_name", default=lock_entities[0]): vol.In(lock_entities),
        })

        return self.async_show_form(step_id="user", data_schema=schema, errors=errors)
