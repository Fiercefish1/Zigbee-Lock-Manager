import logging
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers import entity_registry as er

from .const import DOMAIN, DEFAULT_SLOT_COUNT

_LOGGER = logging.getLogger(__name__)

async def async_setup(hass: HomeAssistant, config: dict) -> bool:
    """Set up the ZHA Lock Manager component via YAML (not UI-based)."""
    _LOGGER.info("Setting up ZHA Lock Manager from YAML is not supported.")
    return True

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
    
    # Dynamically create the helpers (input_booleans, input_numbers)
    await create_helpers(hass, lock_entity_id, slot_count)

    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    _LOGGER.info("Unloading ZHA Lock Manager.")

    # Cleanup automations and helper entities
    await remove_helpers(hass, entry.data.get("lock_entity"), entry.data.get("slot_count"))
    return True

async def create_helpers(hass: HomeAssistant, lock_entity_id: str, slot_count: int):
    """Create the required input_number and input_boolean helpers."""
    for slot in range(1, slot_count + 1):
        input_number_id = f"input_number.{DOMAIN}_slot_{slot}_code"
        input_boolean_id = f"input_boolean.{DOMAIN}_slot_{slot}_enabled"

        _LOGGER.info(f"Creating helpers for slot {slot}: {input_number_id}, {input_boolean_id}")

        # Create input_number for the code slot
        if not hass.states.get(input_number_id):
            await hass.services.async_call(
                "input_number",
                "set_value",
                {
                    "entity_id": input_number_id,
                    "name": f"Code Slot {slot}",
                    "min": 0,
                    "max": 999999,
                    "step": 1,
                },
                blocking=True
            )

        # Create input_boolean for enabling/disabling the code slot
        if not hass.states.get(input_boolean_id):
            await hass.services.async_call(
                "input_boolean",
                "turn_on",
                {
                    "entity_id": input_boolean_id,
                    "name": f"Enable Code Slot {slot}",
                },
                blocking=True
            )

async def remove_helpers(hass: HomeAssistant, lock_entity_id: str, slot_count: int):
    """Remove the dynamically created helpers."""
    entity_registry = er.async_get(hass)
    
    for slot in range(1, slot_count + 1):
        input_number_id = f"input_number.{DOMAIN}_slot_{slot}_code"
        input_boolean_id = f"input_boolean.{DOMAIN}_slot_{slot}_enabled"

        _LOGGER.info(f"Removing helpers for slot {slot}: {input_number_id}, {input_boolean_id}")

        entity_registry.async_remove(input_number_id)
        entity_registry.async_remove(input_boolean_id)

