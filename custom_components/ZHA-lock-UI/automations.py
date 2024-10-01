import logging
from homeassistant.helpers import template

_LOGGER = logging.getLogger(__name__)

async def create_lock_code_automations(hass, slot_count, lock_name, lock_device_id):
    """Dynamically create automations for managing lock codes."""
    for slot in range(1, slot_count + 1):
        await create_clear_lock_code_automation(hass, slot, lock_name)
        await create_update_lock_code_automation(hass, slot, lock_device_id)
        await create_toggle_code_status_automation(hass, slot, lock_name)

        _LOGGER.info(f"Registered automations for slot {slot}")

async def create_clear_lock_code_automation(hass, slot, lock_name):
    """Create an automation for clearing the lock code."""
    automation_config = {
        "alias": f"Clear Lock Code {slot}",
        "trigger": [
            {
                "platform": "state",
                "entity_id": f"input_button.zha_lock_code_clear_{slot}",
                "to": "on",
            }
        ],
        "action": [
            {
                "service": "zha.clear_lock_user_code",
                "data": {
                    "code_slot": slot
                },
                "target": {
                    "entity_id": f"lock.{lock_name}"
                }
            }
        ],
        "mode": "single"
    }
    
    # Use the automation reload service after inserting config
    await hass.services.async_call("automation", "reload")

async def create_update_lock_code_automation(hass, slot, lock_device_id):
    """Create an automation for updating the lock code."""
    automation_config = {
        "alias": f"Update Lock Code {slot}",
        "trigger": [
            {
                "platform": "state",
                "entity_id": f"input_button.zha_lock_code_update_{slot}",
                "to": "on",
            }
        ],
        "action": [
            {
                "service": "zha.set_lock_user_code",
                "data_template": {
                    "code_slot": slot,
                    "user_code": f"{{{{ states('input_text.zha_lock_code_{slot}') }}}}"
                },
                "target": {
                    "device_id": lock_device_id
                }
            }
        ],
        "mode": "single"
    }
    
    # Use the automation reload service after inserting config
    await hass.services.async_call("automation", "reload")

async def create_toggle_code_status_automation(hass, slot, lock_name):
    """Create an automation for toggling the lock code status."""
    automation_config = {
        "alias": f"Toggle Code Status {slot}",
        "trigger": [
            {
                "platform": "state",
                "entity_id": f"input_boolean.zha_lock_code_status_{slot}",
            }
        ],
        "action": [
            {
                "choose": [
                    {
                        "conditions": [
                            {
                                "condition": "state",
                                "entity_id": f"input_boolean.zha_lock_code_status_{slot}",
                                "state": "on"
                            }
                        ],
                        "sequence": [
                            {
                                "service": "zha.enable_lock_user_code",
                                "data": {
                                    "code_slot": slot
                                },
                                "target": {
                                    "entity_id": f"lock.{lock_name}"
                                }
                            }
                        ]
                    },
                    {
                        "conditions": [
                            {
                                "condition": "state",
                                "entity_id": f"input_boolean.zha_lock_code_status_{slot}",
                                "state": "off"
                            }
                        ],
                        "sequence": [
                            {
                                "service": "zha.disable_lock_user_code",
                                "data": {
                                    "code_slot": slot
                                },
                                "target": {
                                    "entity_id": f"lock.{lock_name}"
                                }
                            }
                        ]
                    }
                ]
            }
        ],
        "mode": "single"
    }
    
    # Use the automation reload service after inserting config
    await hass.services.async_call("automation", "reload")

async def remove_lock_code_automations(hass, slot_count):
    """Remove automations for managing lock codes."""
    for slot in range(1, slot_count + 1):
        await remove_automation(hass, f"Clear Lock Code {slot}")
        await remove_automation(hass, f"Update Lock Code {slot}")
        await remove_automation(hass, f"Toggle Code Status {slot}")

async def remove_automation(hass, alias):
    """Helper function to remove an automation by alias."""
    _LOGGER.info(f"Removing automation: {alias}")
    automation_entity = f"automation.{alias.replace(' ', '_').lower()}"
    await hass.services.async_call("automation", "turn_off", {"entity_id": automation_entity})
