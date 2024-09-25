import logging

_LOGGER = logging.getLogger(__name__)

async def create_automations(hass, domain: str, slot_count: int, lock_entity_id: str):
    """Dynamically create automations based on the number of users."""
    automation_service = "automation"

    for slot in range(1, slot_count + 1):
        # Automation for updating lock code
        update_automation = {
            "alias": f"Zigbee Lock: Update Lock Code Slot {slot}",
            "trigger": [
                {
                    "platform": "state",
                    "entity_id": f"input_button.{domain}_code_update_{slot}",
                }
            ],
            "action": [
                {
                    "service": "zha.set_lock_user_code",
                    "data_template": {
                        "code_slot": f"{slot}",
                        "user_code": f"{{{{ states('input_text.{domain}_code_{slot}') }}}}"
                    },
                    "target": {
                        "entity_id": lock_entity_id
                    }
                }
            ],
            "mode": "single"
        }

        await hass.services.async_call(automation_service, "reload", blocking=True)
        _LOGGER.info(f"Created automation: {update_automation['alias']}")

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
        update_automation_id = f"automation.zigbee_lock_update_lock_code_slot_{slot}"
        status_automation_id = f"automation.zigbee_lock_toggle_code_status_slot_{slot}"

        _LOGGER.info(f"Removing automation: {update_automation_id}")
        _LOGGER.info(f"Removing automation: {status_automation_id}")

        entity_registry.async_remove(update_automation_id)
        entity_registry.async_remove(status_automation_id)
