import logging
from .automations import create_lock_code_automations, remove_lock_code_automations
from .helpers import create_lock_code_helpers, remove_lock_code_helpers

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass, entry):
    """Set up Zigbee Lock Manager from a config entry."""
    slot_count = entry.data.get("slot_count")
    lock_name = entry.data.get("lock_name")
    lock_device_id = entry.data.get("lock_device_id")

    # Log config entry for debugging
    _LOGGER.debug(f"Setting up entry: Slot count={slot_count}, Lock name={lock_name}, Lock device ID={lock_device_id}")

    # Create lock code helpers (input_text, input_boolean, etc.)
    await create_lock_code_helpers(hass, slot_count, entry, async_add_entities=None)

    # Create lock code automations (trigger, action logic)
    await create_lock_code_automations(hass, slot_count, lock_name, lock_device_id)

    return True

async def async_unload_entry(hass, entry):
    """Unload Zigbee Lock Manager and clean up."""
    slot_count = entry.data.get("slot_count")

    # Remove lock code helpers
    await remove_lock_code_helpers(hass, slot_count, entry)

    # Remove lock code automations
    await remove_lock_code_automations(hass, slot_count)

    return True
