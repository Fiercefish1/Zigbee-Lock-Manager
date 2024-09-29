import logging
from homeassistant.helpers.entity_registry import async_get

_LOGGER = logging.getLogger(__name__)

async def create_lock_code_helpers(hass, slot_count, config_entry):
    """Dynamically create lock code helpers based on the slot count."""
    entity_registry = async_get(hass)

    for slot in range(1, slot_count + 1):
        # Create input_text for Lock User
        await create_input_text(hass, entity_registry, config_entry, slot, "user", "mdi:account", "Lock User")

        # Create input_text for Lock Code
        await create_input_text(hass, entity_registry, config_entry, slot, "code", "mdi:dialpad", "Lock Code")

        # Create input_boolean for Code Status
        await create_input_boolean(hass, entity_registry, config_entry, slot, "status", "Code Status")

        # Create input_button for Code Update
        await create_input_button(hass, entity_registry, config_entry, slot, "update", "Update Code")

        # Create input_button for Code Clear
        await create_input_button(hass, entity_registry, config_entry, slot, "clear", "Clear Code")


async def create_input_text(hass, entity_registry, config_entry, slot, name_type, icon, name_prefix):
    """Helper function to create an input_text entity."""
    unique_id = f"zha_lock_{name_type}_{slot}"
    entity_id = f"input_text.zha_lock_{name_type}_{slot}"

    if not entity_registry.async_get(entity_id):
        entity_registry.async_get_or_create(
            domain="input_text",
            platform="custom_input_text",
            unique_id=unique_id,
            config_entry=config_entry
        )

    # Set entity state and friendly name
    hass.states.async_set(entity_id, '', {
        'friendly_name': f'{name_prefix} {slot}',
        'max': 25,
        'icon': icon,
        'mode': 'text'
    })

async def create_input_boolean(hass, entity_registry, config_entry, slot, name_type, name_prefix):
    """Helper function to create an input_boolean entity."""
    unique_id = f"zha_lock_{name_type}_{slot}"
    entity_id = f"input_boolean.zha_lock_{name_type}_{slot}"

    if not entity_registry.async_get(entity_id):
        entity_registry.async_get_or_create(
            domain="input_boolean",
            platform="custom_input_boolean",
            unique_id=unique_id,
            config_entry=config_entry
        )

    # Set entity state and friendly name
    hass.states.async_set(entity_id, '', {
        'friendly_name': f'{name_prefix} {slot}',
        'initial': False
    })

async def create_input_button(hass, entity_registry, config_entry, slot, name_type, name_prefix):
    """Helper function to create an input_button entity."""
    unique_id = f"zha_lock_{name_type}_{slot}"
    entity_id = f"input_button.zha_lock_{name_type}_{slot}"

    if not entity_registry.async_get(entity_id):
        entity_registry.async_get_or_create(
            domain="input_button",
            platform="custom_input_button",
            unique_id=unique_id,
            config_entry=config_entry
        )

    # Set entity state and friendly name
    hass.states.async_set(entity_id, '', {
        'friendly_name': f'{name_prefix} {slot}'
    })
