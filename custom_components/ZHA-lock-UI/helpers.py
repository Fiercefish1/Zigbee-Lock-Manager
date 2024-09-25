import logging

_LOGGER = logging.getLogger(__name__)

async def create_helpers(hass, domain, slot_count):
    """Create the required input_text, input_boolean, and input_button helpers."""
    for slot in range(1, slot_count + 1):
        user_input_text = f"input_text.{domain}_user_{slot}"
        code_input_text = f"input_text.{domain}_code_{slot}"
        code_status_boolean = f"input_boolean.{domain}_code_status_{slot}"
        code_update_button = f"input_button.{domain}_code_update_{slot}"

        _LOGGER.info(f"Creating helpers for slot {slot}: {user_input_text}, {code_input_text}, {code_status_boolean}, {code_update_button}")

        # Create input_text for the user name
        if not hass.states.get(user_input_text):
            await hass.services.async_call(
                "input_text",
                "set_value",
                {
                    "entity_id": user_input_text,
                    "name": f"User {slot}",
                    "icon": "mdi:account",
                },
                blocking=True
            )

        # Create input_text for the code
        if not hass.states.get(code_input_text):
            await hass.services.async_call(
                "input_text",
                "set_value",
                {
                    "entity_id": code_input_text,
                    "name": f"Code {slot}",
                    "min": 0,
                    "max": 999999,
                    "pattern": r"\d*",
                },
                blocking=True
            )

        # Create input_boolean for enabling/disabling the code slot
        if not hass.states.get(code_status_boolean):
            await hass.services.async_call(
                "input_boolean",
                "turn_on",
                {
                    "entity_id": code_status_boolean,
                    "name": f"Code Status {slot}",
                    "icon": "mdi:lock",
                },
                blocking=True
            )

        # Create input_button for updating the code
        if not hass.states.get(code_update_button):
            await hass.services.async_call(
                "input_button",
                "set",
                {
                    "entity_id": code_update_button,
                    "name": f"Update Code {slot}",
                    "icon": "mdi:upload",
                },
                blocking=True
            )

async def remove_helpers(hass, domain, slot_count):
    """Remove the dynamically created helpers."""
    entity_registry = hass.helpers.entity_registry.async_get(hass)

    for slot in range(1, slot_count + 1):
        user_input_text = f"input_text.{domain}_user_{slot}"
        code_input_text = f"input_text.{domain}_code_{slot}"
        code_status_boolean = f"input_boolean.{domain}_code_status_{slot}"
        code_update_button = f"input_button.{domain}_code_update_{slot}"

        _LOGGER.info(f"Removing helpers for slot {slot}: {user_input_text}, {code_input_text}, {code_status_boolean}, {code_update_button}")

        entity_registry.async_remove(user_input_text)
        entity_registry.async_remove(code_input_text)
        entity_registry.async_remove(code_status_boolean)
        entity_registry.async_remove(code_update_button)
