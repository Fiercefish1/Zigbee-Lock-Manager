import logging
from .helpers import create_lock_code_helpers, remove_lock_code_helpers
from .automations import create_lock_code_automations, remove_lock_code_automations

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass, entry):
    """Set up the integration from a config entry."""
    slot_count = entry.data.get("slot_count")
    lock_name = entry.data.get("lock_name")
    lock_device_id = entry.data.get("lock_device_id")

    # Create the helpers for lock codes
    await create_lock_code_helpers(hass, slot_count, entry)

    # Create automations based on the lock codes
    await create_lock_code_automations(hass, slot_count, lock_name, lock_device_id)

    return True

async def async_unload_entry(hass, entry):
    """Unload the integration and clean up entities."""
    slot_count = entry.data.get("slot_count")
    
    # Remove the helpers and automations
    await remove_lock_code_helpers(hass, slot_count, entry)
    await remove_lock_code_automations(hass, slot_count)

    return True
