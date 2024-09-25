import voluptuous as vol
from homeassistant import config_entries
from homeassistant.core import callback
from .const import DOMAIN

class LockManagerConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle the configuration flow for ZHA Lock Manager."""

    async def async_step_user(self, user_input=None):
        """Step to configure the integration via the UI."""
        if user_input is not None:
            return self.async_create_entry(title="ZHA Lock Manager", data=user_input)

        # Get list of locks available to select
        locks = [entity_id for entity_id in self.hass.states.async_entity_ids('lock')]

        schema = vol.Schema({
            vol.Required("lock_entity"): vol.In(locks),
            vol.Required("slot_count", default=5): vol.All(vol.Coerce(int), vol.Range(min=1, max=10)),
        })

        return self.async_show_form(step_id="user", data_schema=schema)
