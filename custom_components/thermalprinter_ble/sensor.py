"""Sensor platform for Thermal Printer."""
from __future__ import annotations

from homeassistant.components.sensor import SensorEntity, SensorEntityDescription
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN, STATE_ERROR, STATE_IDLE, STATE_OFFLINE, STATE_PRINTING
from .coordinator import ThermalPrinterDataUpdateCoordinator

SENSOR_TYPES: tuple[SensorEntityDescription, ...] = (
    SensorEntityDescription(
        key="status",
        name="Status",
        icon="mdi:printer",
    ),
    SensorEntityDescription(
        key="error",
        name="Error",
        icon="mdi:alert-circle",
    ),
)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Thermal Printer sensor based on a config entry."""
    coordinator: ThermalPrinterDataUpdateCoordinator = hass.data[DOMAIN][entry.entry_id]

    async_add_entities(
        ThermalPrinterSensor(coordinator, description) for description in SENSOR_TYPES
    )


class ThermalPrinterSensor(CoordinatorEntity[ThermalPrinterDataUpdateCoordinator], SensorEntity):
    """Representation of a Thermal Printer sensor."""

    def __init__(
        self,
        coordinator: ThermalPrinterDataUpdateCoordinator,
        description: SensorEntityDescription,
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)
        self.entity_description = description
        self._attr_unique_id = (
            f"{coordinator.ble_device.address}_{description.key}"
        )
        self._attr_device_info = {
            "identifiers": {(DOMAIN, coordinator.ble_device.address)},
            "name": "Thermal Printer (BLE)",
            "manufacturer": "Generic",
            "model": "58mm Thermal Printer",
        }

    @property
    def native_value(self) -> str | None:
        """Return the state of the sensor."""
        if not self.coordinator.data:
            return STATE_OFFLINE

        status = self.coordinator.data

        if self.entity_description.key == "status":
            if status.has_error:
                return STATE_ERROR
            elif status.is_idle:
                return STATE_IDLE
            elif status.has_data:
                return STATE_PRINTING
            else:
                return STATE_IDLE

        elif self.entity_description.key == "error":
            if status.has_error:
                return str(status)
            return "No Error"

        return None

    @property
    def available(self) -> bool:
        """Return True if entity is available."""
        return self.coordinator.last_update_success
