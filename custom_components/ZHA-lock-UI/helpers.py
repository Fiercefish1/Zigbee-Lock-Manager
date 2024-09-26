import logging

_LOGGER = logging.getLogger(__name__)

async def create_input_text(hass, entity_id, name, min_value=0, max_value=100):
    """Dynamically create an input_text entity."""
    if not hass.states.get(entity_id):
        _LOGGER.debug(f"Creating input_text {entity_id}")
        await hass.services.async_call(
            "input_text",
            "create",
            {
                "name": name,
                "entity_id": entity_id,
                "min": min_value,
                "max": max_value,
                "pattern": ".*"  # You can adjust this pattern based on your needs
            },
            blocking=True
        )

async def create_input_boolean(hass, entity_id, name):
    """Dynamically create an input_boolean entity."""
    if not hass.states.get(entity_id):
        _LOGGER.debug(f"Creating input_boolean {entity_id}")
        await hass.services.async_call(
            "input_boolean",
            "create",
            {
                "name": name,
                "entity_id": entity_id,
            },
            blocking=True
        )

async def create_helpers(hass, domain, slot_count):
    """Dynamically create the required input_text and input_boolean helpers."""
    for slot in range(1, slot_count + 1):
        user_input_text = f"input_text.{domain}_user_{slot}"
        code_input_text = f"input_text.{domain}_code_{slot}"
        code_status_boolean = f"input_boolean.{domain}_code_status_{slot}"

        _LOGGER.info(f"Creating helpers for slot {slot}: {user_input_text}, {code_input_text}, {code_status_boolean}")

        # Dynamically create input_text for the user name
        await create_input_text(hass, user_input_text, f"User {slot}")

        # Dynamically create input_text for the code
        await create_input_text(hass, code_input_text, f"Code {slot}", min_value=0, max_value=6)

        # Dynamically create input_boolean for enabling/disabling the code slot
        await create_input_boolean(hass, code_status_boolean, f"Code Status {slot}")

async def remove_helpers(hass, domain, slot_count):
    """Remove the dynamically created helpers."""
    for slot in range(1, slot_count + 1):
        user_input_text = f"input_text.{domain}_user_{slot}"
        code_input_text = f"input_text.{domain}_code_{slot}"
        code_status_boolean = f"input_boolean.{domain}_code_status_{slot}"

        _LOGGER.info(f"Removing helpers for slot {slot}: {user_input_text}, {code_input_text}, {code_status_boolean}")

        # There is no delete service, but we can reload them to remove
        if hass.states.get(user_input_text):
            await hass.services.async_call(
                "input_text",
                "reload",
                blocking=True
            )
        if hass.states.get(code_input_text):
            await hass.services.async_call(
                "input_text",
                "reload",
                blocking=True
            )
        if hass.states.get(code_status_boolean):
            await hass.services.async_call(
                "input_boolean",
                "reload",
                blocking=True
            )
