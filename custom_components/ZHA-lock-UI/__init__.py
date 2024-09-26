import logging
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers import discovery
from homeassistant.helpers.entity_registry import async_get_registry
from homeassistant.helpers.service import async_register_admin_service
from .const import DOMAIN, DEFAULT_SLOT_COUNT, PLATFORMS
from .automations import create_scripts, remove_scripts

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up the integration from a config entry (UI-based)."""
    _LOGGER.info("Setting up ZHA Lock Manager from config entry.")

    # Delay importing helpers to avoid circular import issues
    from .helpers import create_helpers, remove_helpers

    lock_entity_id = entry.data.get("lock_entity")
    slot_count = entry.data.get("slot_count", DEFAULT_SLOT_COUNT)

    # Store config entry data in hass.data to access later
    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = {
        "lock_entity": lock_entity_id,
        "slot_count": slot_count,
    }

    # Dynamically create the helpers (input_text, input_boolean)
    await create_helpers(hass, DOMAIN, slot_count)

    # Dynamically create the scripts
    await create_scripts(hass, DOMAIN, slot_count, lock_entity_id)

    # Setup platforms (if required)
    hass.config_entries.async_setup_platforms(entry, PLATFORMS)

    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    _LOGGER.info("Unloading ZHA Lock Manager.")

    # Delay importing helpers to avoid circular import issues
    from .helpers import remove_helpers

    # Remove helpers and scripts
    slot_count = hass.data[DOMAIN][entry.entry_id]["slot_count"]
    await remove_helpers(hass, DOMAIN, slot_count)
    await remove_scripts(hass, DOMAIN, slot_count)

    # Unload platforms
    return await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
