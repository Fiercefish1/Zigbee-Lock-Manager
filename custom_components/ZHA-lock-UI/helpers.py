import logging
from homeassistant.components.input_text import InputText
from homeassistant.components.input_boolean import InputBoolean
from homeassistant.components.input_button import InputButton
from homeassistant.helpers.entity import Entity
from homeassistant.helpers.entity_registry import async_get

_LOGGER = logging.getLogger(__name__)

async def create_lock_code_helpers(hass, slot_count, config_entry, async_add_entities=None):
    """Dynamically create lock code helpers based on the slot count."""
    entity_registry = async_get(hass)

    for slot in range(1, slot_count + 1):
        # Create the entities
        user_input_text = LockUserInputText(config_entry, slot)
        code_input_text = LockCodeInputText(config_entry, slot)
        status_input_boolean = LockCodeStatusInputBoolean(config_entry, slot)
        update_input_button = LockCodeUpdateInputButton(config_entry, slot)
        clear_input_button = LockCodeClearInputButton(config_entry, slot)

        # Manually suggest the object_id to avoid automatic domain prefixing
        entity_registry.async_get_or_create(
            domain="input_text",
            platform="input_text",
            unique_id=user_input_text.unique_id,
            suggested_object_id=f"zha_lock_user_{slot}",  # Correct name
            config_entry=config_entry
        )
        entity_registry.async_get_or_create(
            domain="input_text",
            platform="input_text",
            unique_id=code_input_text.unique_id,
            suggested_object_id=f"zha_lock_code_{slot}",  # Correct name
            config_entry=config_entry
        )
        entity_registry.async_get_or_create(
            domain="input_boolean",
            platform="input_boolean",
            unique_id=status_input_boolean.unique_id,
            suggested_object_id=f"zha_lock_code_status_{slot}",  # Correct name
            config_entry=config_entry
        )
        entity_registry.async_get_or_create(
            domain="input_button",
            platform="input_button",
            unique_id=update_input_button.unique_id,
            suggested_object_id=f"zha_lock_code_update_{slot}",  # Correct name
            config_entry=config_entry
        )
        entity_registry.async_get_or_create(
            domain="input_button",
            platform="input_button",
            unique_id=clear_input_button.unique_id,
            suggested_object_id=f"zha_lock_code_clear_{slot}",  # Correct name
            config_entry=config_entry
        )

        _LOGGER.info(f"Registered entities for slot {slot}")

class LockUserInputText(InputText):
    """Representation of a Lock User input_text."""
    def __init__(self, config_entry, slot):
        self._config_entry = config_entry
        self._slot = slot
        self._state = ''
        self.entity_id = f"input_text.zha_lock_user_{slot}"
        self._attr_unique_id = f"zha_lock_user_{slot}"

    @property
    def name(self):
        """Return the name of the entity."""
        return f"Lock User {self._slot}"

    @property
    def state(self):
        """Return the state of the entity."""
        return self._state

    @property
    def unique_id(self):
        """Return the unique ID for the entity."""
        return self._attr_unique_id

    async def async_set_value(self, value):
        """Set the value of the input_text."""
        self._state = value
        self.async_write_ha_state()


class LockCodeInputText(InputText):
    """Representation of a Lock Code input_text."""
    def __init__(self, config_entry, slot):
        self._config_entry = config_entry
        self._slot = slot
        self._state = ''
        self.entity_id = f"input_text.zha_lock_code_{slot}"
        self._attr_unique_id = f"zha_lock_code_{slot}"

    @property
    def name(self):
        """Return the name of the entity."""
        return f"Lock Code {self._slot}"

    @property
    def state(self):
        """Return the state of the entity."""
        return self._state

    @property
    def unique_id(self):
        """Return the unique ID for the entity."""
        return self._attr_unique_id

    async def async_set_value(self, value):
        """Set the value of the input_text."""
        self._state = value
        self.async_write_ha_state()


class LockCodeStatusInputBoolean(InputBoolean):
    """Representation of a Lock Code Status input_boolean."""
    def __init__(self, config_entry, slot):
        self._config_entry = config_entry
        self._slot = slot
        self._state = False
        self.entity_id = f"input_boolean.zha_lock_code_status_{slot}"
        self._attr_unique_id = f"zha_lock_code_status_{slot}"

    @property
    def name(self):
        """Return the name of the entity."""
        return f"Code Status {self._slot}"

    @property
    def state(self):
        """Return the state of the entity."""
        return self._state

    @property
    def unique_id(self):
        """Return the unique ID for the entity."""
        return self._attr_unique_id

    async def async_set_value(self, value):
        """Set the value of the input_boolean."""
        self._state = value
        self.async_write_ha_state()


class LockCodeUpdateInputButton(InputButton):
    """Representation of a Lock Code Update input_button."""
    def __init__(self, config_entry, slot):
        self._config_entry = config_entry
        self._slot = slot
        self.entity_id = f"input_button.zha_lock_code_update_{slot}"
        self._attr_unique_id = f"zha_lock_code_update_{slot}"

    @property
    def name(self):
        """Return the name of the entity."""
        return f"Update Code {self._slot}"

    async def async_press(self):
        """Handle the press of the input_button."""
        _LOGGER.info(f"Lock code update button {self._slot} pressed")


class LockCodeClearInputButton(InputButton):
    """Representation of a Lock Code Clear input_button."""
    def __init__(self, config_entry, slot):
        self._config_entry = config_entry
        self._slot = slot
        self.entity_id = f"input_button.zha_lock_code_clear_{slot}"
        self._attr_unique_id = f"zha_lock_code_clear_{slot}"

    @property
    def name(self):
        """Return the name of the entity."""
        return f"Clear Code {self._slot}"

    async def async_press(self):
        """Handle the press of the input_button."""
        _LOGGER.info(f"Lock code clear button {self._slot} pressed")


async def remove_lock_code_helpers(hass, slot_count, config_entry):
    """Remove lock code helpers."""
    entity_registry = async_get(hass)

    for slot in range(1, slot_count + 1):
        # Remove entities for Lock User, Lock Code, etc.
        await remove_entity(hass, entity_registry, f"input_text.zha_lock_user_{slot}")
        await remove_entity(hass, entity_registry, f"input_text.zha_lock_code_{slot}")
        await remove_entity(hass, entity_registry, f"input_boolean.zha_lock_code_status_{slot}")
        await remove_entity(hass, entity_registry, f"input_button.zha_lock_code_update_{slot}")
        await remove_entity(hass, entity_registry, f"input_button.zha_lock_code_clear_{slot}")


async def remove_entity(hass, entity_registry, entity_id):
    """Helper function to remove an entity."""
    if entity := entity_registry.async_get(entity_id):
        entity_registry.async_remove(entity_id)
        _LOGGER.info(f"Removed entity: {entity_id}")
    else:
        _LOGGER.warning(f"Entity {entity_id} not found.")
