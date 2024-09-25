import logging
from homeassistant.helpers.entity import Entity
from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass, config_entry, async_add_entities):
    """Set up the sensors from a config entry."""
    _LOGGER.info("Setting up ZHA Lock Manager sensors")

    # Retrieve the number of slots from the config entry
    slot_count = hass.data[DOMAIN][config_entry.entry_id]["slot_count"]
    lock_entity_id = hass.data[DOMAIN][config_entry.entry_id]["lock_entity"]

    # Create a sensor for each lock code slot
    sensors = []
    for slot in range(1, slot_count + 1):
        sensors.append(LockCodeSensor(hass, lock_entity_id, slot))

    # Add all the sensors
    async_add_entities(sensors, update_before_add=True)


class LockCodeSensor(Entity):
    """Representation of a lock code slot sensor."""

    def __init__(self, hass, lock_entity_id, slot):
        """Initialize the lock code sensor."""
        self._hass = hass
        self._lock_entity_id = lock_entity_id
        self._slot = slot
        self._state = None
        self._name = f"Lock Code Slot {slot} Status"
        self._attr_unique_id = f"{DOMAIN}_{lock_entity_id}_slot_{slot}_status"

    @property
    def name(self):
        """Return the name of the sensor."""
        return self._name

    @property
    def state(self):
        """Return the state of the sensor."""
        return self._state

    @property
    def unique_id(self):
        """Return a unique ID for the sensor."""
        return self._attr_unique_id

    @property
    def icon(self):
        """Return the icon of the sensor."""
        return "mdi:lock" if self._state == "set" else "mdi:lock-open"

    @property
    def extra_state_attributes(self):
        """Return additional state attributes."""
        return {
            "slot_number": self._slot,
            "lock_entity_id": self._lock_entity_id,
        }

    def update(self):
        """Update the state of the sensor."""
        input_number_entity_id = f"input_number.{DOMAIN}_slot_{self._slot}_code"
        input_boolean_entity_id = f"input_boolean.{DOMAIN}_slot_{self._slot}_enabled"

        # Retrieve the current state of the input_number and input_boolean helpers
        input_number_state = self._hass.states.get(input_number_entity_id)
        input_boolean_state = self._hass.states.get(input_boolean_entity_id)

        if input_number_state and input_boolean_state:
            if input_boolean_state.state == "on" and int(input_number_state.state) > 0:
                self._state = "set"  # Code is set
            else:
                self._state = "unset"  # Code is not set or disabled
        else:
            _LOGGER.warning(f"Helper entities for slot {self._slot} not found")

