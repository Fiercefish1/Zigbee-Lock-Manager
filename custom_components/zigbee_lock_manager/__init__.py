import logging
import asyncio
from homeassistant.core import HomeAssistant
from .zha_manager import (
    create_helpers_and_automations,
    remove_helpers_and_automations,
    link_helpers_to_device,
    create_dashboard_yaml  # Import the dashboard creation function
)
from homeassistant.helpers import device_registry as dr

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass, entry):
    """Set up Zigbee Lock Manager from a config entry."""
    slot_count = entry.data.get("slot_count")
    lock_name = entry.data.get("lock_name")

    # Step 1: Create the YAML-based helpers and automations
    await create_helpers_and_automations(hass, slot_count, lock_name, entry)

    # Step 2: Reload automations and input helpers
    await hass.services.async_call("automation", "reload")
    await hass.services.async_call("input_boolean", "reload")
    await hass.services.async_call("input_text", "reload")
    await hass.services.async_call("input_button", "reload")

    # Step 3: Introduce a small delay to ensure entities are fully loaded
    await asyncio.sleep(2)  # Adjust the sleep duration if necessary

    # Step 4: Register a device for the lock manager
    device_registry = dr.async_get(hass)
    device = device_registry.async_get_or_create(
        config_entry_id=entry.entry_id,
        identifiers={(entry.domain, lock_name)},
        manufacturer="YourManufacturer",
        name=f"Zigbee Lock Manager ({lock_name})",
        model="Zigbee Lock",
        sw_version="1.0",
    )

    # Step 5: Link YAML-created helpers to the device
    for slot in range(1, slot_count + 1):
        await link_helpers_to_device(hass, entry, lock_name, slot, device)

    # Step 6: Create the dashboard YAML file
    await create_dashboard_yaml(hass, slot_count, lock_name)

    _LOGGER.info("Zigbee Lock Manager setup complete")
    return True

async def async_unload_entry(hass: HomeAssistant, entry):
    """Unload Zigbee Lock Manager and clean up."""

    _LOGGER.debug("Unloading Zigbee Lock Manager.")

    # Remove helpers and automations
    await remove_helpers_and_automations(hass, entry.data.get("lock_name"), entry.data.get("slot_count"))

    _LOGGER.info("Zigbee Lock Manager unloaded.")
    return True
