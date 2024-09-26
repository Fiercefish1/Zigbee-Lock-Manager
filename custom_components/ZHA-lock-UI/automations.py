import logging

_LOGGER = logging.getLogger(__name__)

async def create_automations(hass, domain: str, slot_count: int, lock_entity_id: str):
    """Dynamically create automations for toggling lock code status based on input_boolean."""
    automation_service = "automation"

    for slot in range(1, slot_count + 1):
        # Automation for toggling lock code status
        status_automation = {
            "alias": f"Zigbee Lock: Toggle Code Status Slot {slot}",
            "trigger": [
                {
                    "platform": "state",
                    "entity_id": f"input_boolean.{domain}_code_status_{slot}",
                }
            ],
            "action": [
                {
                    "choose": [
                        {
                            "conditions": [
                                {
                                    "condition": "template",
                                    "value_template": "{{ trigger.to_state.state == 'on' }}"
                                }
                            ],
                            "sequence": [
                                {
                                    "service": "zha.enable_lock_user_code",
                                    "data": {
                                        "code_slot": slot
                                    },
                                    "target": {
                                        "entity_id": lock_entity_id
                                    }
                                }
                            ]
                        },
                        {
                            "conditions": [
                                {
                                    "condition": "template",
                                    "value_template": "{{ trigger.to_state.state == 'off' }}"
                                }
                            ],
                            "sequence": [
                                {
                                    "service": "zha.disable_lock_user_code",
                                    "data": {
                                        "code_slot": slot
                                    },
                                    "target": {
                                        "entity_id": lock_entity_id
                                    }
                                }
                            ]
                        }
                    ]
                }
            ],
            "mode": "single"
        }

        await hass.services.async_call(automation_service, "reload", blocking=True)
        _LOGGER.info(f"Created automation: {status_automation['alias']}")

async def remove_automations(hass, domain: str, slot_count: int):
    """Remove the automations when the integration is removed."""
    entity_registry = hass.helpers.entity_registry.async_get(hass)

    for slot in range(1, slot_count + 1):
        status_automation_id = f"automation.zigbee_lock_toggle_code_status_slot_{slot}"

        _LOGGER.info(f"Removing automation: {status_automation_id}")
        entity_registry.async_remove(status_automation_id)


async def create_scripts(hass, domain: str, slot_count: int, lock_entity_id: str):
    """Dynamically create scripts for updating lock codes."""
    for slot in range(1, slot_count + 1):
        script_id = f"{domain}_update_lock_code_slot_{slot}"
        user_code_template = f"{{{{ states('input_text.{domain}_code_{slot}') }}}}"

        _LOGGER.info(f"Creating script: {script_id}")

        script = {
            "alias": f"Update Lock Code Slot {slot}",
            "sequence": [
                {
                    "service": "zha.set_lock_user_code",
                    "data_template": {
                        "code_slot": slot,
                        "user_code": user_code_template,
                    },
                    "target": {
                        "entity_id": lock_entity_id
                    }
                }
            ]
        }

        # Create the script dynamically in Home Assistant
        await hass.services.async_call(
            "script",
            "reload",  # This will reload the scripts after creation
            blocking=True
        )

        # Logging for debugging purposes
        _LOGGER.info(f"Script {script_id} has been created.")


async def remove_scripts(hass, domain: str, slot_count: int):
    """Remove the dynamically created scripts."""
    for slot in range(1, slot_count + 1):
        script_id = f"script.{domain}_update_lock_code_slot_{slot}"
        _LOGGER.info(f"Removing script: {script_id}")

        await hass.services.async_call(
            "script",
            "reload",  # Reloading after removing the script
            blocking=True
        )
