import logging

_LOGGER = logging.getLogger(__name__)

async def create_lock_code_automations(hass, slot_count, lock_name, lock_device_id):
    """Dynamically create automations for managing lock codes."""

    # Gather triggers for each slot for each automation
    clear_triggers = []
    update_triggers = []
    toggle_triggers = []

    for slot in range(1, slot_count + 1):
        # Add triggers for "Clear Lock Code"
        clear_triggers.append({
            "platform": "state",
            "entity_id": f"input_button.zha_lock_code_clear_{slot}",
        })

        # Add triggers for "Update Lock Code"
        update_triggers.append({
            "platform": "state",
            "entity_id": f"input_button.zha_lock_code_update_{slot}",
        })

        # Add triggers for "Toggle Code Status"
        toggle_triggers.append({
            "platform": "state",
            "entity_id": f"input_boolean.zha_lock_code_status_{slot}",
        })

    # Create "Clear Lock Code" automation for all slots
    clear_automation = {
        "alias": "Zigbee Lock: Clear Lock Code",
        "trigger": clear_triggers,
        "action": [
            # Step 1: Clear the lock user code
            {
                "service": "zha.clear_lock_user_code",
                "data_template": {
                    "code_slot": "{{ trigger.entity_id.split('_')[-1] | int }}"
                },
                "target": {
                    "entity_id": f"lock.{lock_name}"
                }
            },
            # Step 2: Clear the input_text for Lock User
            {
                "service": "input_text.set_value",
                "data": {
                    "value": ""
                },
                "target": {
                    "entity_id": "{{ 'input_text.zha_lock_user_' + trigger.entity_id.split('_')[-1] }}"
                }
            },
            # Step 3: Clear the input_text for Lock Code
            {
                "service": "input_text.set_value",
                "data": {
                    "value": ""
                },
                "target": {
                    "entity_id": "{{ 'input_text.zha_lock_code_' + trigger.entity_id.split('_')[-1] }}"
                }
            }
        ],
        "mode": "single"
    }
    _LOGGER.info(f"Created automation: {clear_automation['alias']}")

    # Create "Update Lock Code" automation for all slots
    update_automation = {
        "alias": "Zigbee Lock: Update Lock Code",
        "trigger": update_triggers,
        "action": [
            {
                "service": "zha.set_lock_user_code",
                "data_template": {
                    "code_slot": "{{ trigger.entity_id.split('_')[-1] | int }}",
                    "user_code": "{{ states(f'input_text.zha_lock_code_' + trigger.entity_id.split('_')[-1]) }}"
                },
                "target": {
                    "device_id": lock_device_id
                }
            }
        ],
        "mode": "single"
    }
    _LOGGER.info(f"Created automation: {update_automation['alias']}")

    # Create "Toggle Code Status" automation for all slots
    status_automation = {
        "alias": "Zigbee Lock: Toggle Code Status",
        "trigger": toggle_triggers,
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
                                "data_template": {
                                    "code_slot": "{{ trigger.entity_id.split('_')[-1] | int }}"
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
                                "condition": "template",
                                "value_template": "{{ trigger.to_state.state == 'off' }}"
                            }
                        ],
                        "sequence": [
                            {
                                "service": "zha.disable_lock_user_code",
                                "data_template": {
                                    "code_slot": "{{ trigger.entity_id.split('_')[-1] | int }}"
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
    _LOGGER.info(f"Created automation: {status_automation['alias']}")

    # Reload automations after creation
    await hass.services.async_call("automation", "reload", blocking=True)
    _LOGGER.info("Automations reloaded after creation.")


async def remove_lock_code_automations(hass, slot_count):
    """Remove automations for managing lock codes."""
    for slot in range(1, slot_count + 1):
        # Use the automation entity_id format to remove
        entity_id = f"automation.zigbee_lock_manage_slot_{slot}"
        await remove_entity(hass, entity_id)


async def remove_entity(hass, entity_id):
    """Helper function to remove an automation."""
    automation_service = "automation"
    automation_reload = "reload"
    _LOGGER.info(f"Removing automation: {entity_id}")

    # Call the service to reload the automation after removal
    await hass.services.async_call(automation_service, automation_reload, blocking=True)
