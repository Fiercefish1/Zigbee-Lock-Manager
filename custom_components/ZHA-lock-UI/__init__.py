import logging
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from .const import DOMAIN, DEFAULT_SLOT_COUNT
from .helpers import create_helpers, remove_helpers
from .automations import create_automations, remove_automations

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up the integration from a config entry (UI-based)."""
    _LOGGER.info("Setting up ZHA Lock Manager from config entry.")

    lock_entity_id = entry.data.get("lock_entity")
    slot_count = entry.data.get("slot_count", DEFAULT_SLOT_COUNT)

    # Store config entry data in hass.data to access later
    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = {
        "lock_entity": lock_entity_id,
        "slot_count": slot_count,
    }

    # Dynamically create the helpers (input_text, input_boolean, input_button)
    await create_helpers(hass, DOMAIN, slot_count)

    # Dynamically create the automations
    await create_automations(hass, DOMAIN, slot_count, lock_entity_id)

    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    _LOGGER.info("Unloading ZHA Lock Manager.")

    # Remove helpers and automations
    slot_count = hass.data[DOMAIN][entry.entry_id]["slot_count"]
    await remove_helpers(hass, DOMAIN, slot_count)
    await remove_automations(hass, DOMAIN, slot_count)

    return True
