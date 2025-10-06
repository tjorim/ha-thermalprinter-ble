"""The Thermal Printer (BLE) integration."""
from __future__ import annotations

import logging
from typing import Any

from homeassistant.components import bluetooth
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import ConfigEntryNotReady

from .const import DOMAIN
from .coordinator import ThermalPrinterDataUpdateCoordinator

_LOGGER = logging.getLogger(__name__)

PLATFORMS: list[Platform] = [Platform.SENSOR]


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Thermal Printer from a config entry."""
    address: str = entry.data["address"]

    # Check if device is available
    ble_device = bluetooth.async_ble_device_from_address(hass, address, connectable=True)
    if not ble_device:
        raise ConfigEntryNotReady(f"Could not find thermal printer with address {address}")

    # Create coordinator
    coordinator = ThermalPrinterDataUpdateCoordinator(hass, ble_device)

    try:
        await coordinator.async_config_entry_first_refresh()
    except Exception as err:
        raise ConfigEntryNotReady(f"Failed to connect to printer: {err}") from err

    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = coordinator

    # Set up platforms
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    # Register services
    await async_setup_services(hass, coordinator)

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    if unload_ok := await hass.config_entries.async_unload_platforms(entry, PLATFORMS):
        coordinator: ThermalPrinterDataUpdateCoordinator = hass.data[DOMAIN].pop(entry.entry_id)
        await coordinator.async_shutdown()

    return unload_ok


async def async_setup_services(
    hass: HomeAssistant, coordinator: ThermalPrinterDataUpdateCoordinator
) -> None:
    """Set up services for the integration."""

    async def handle_print_text(call: Any) -> None:
        """Handle the print_text service call."""
        text = call.data.get("text", "")
        font_size = call.data.get("font_size", 24)

        await coordinator.print_text(text, font_size)

    async def handle_print_image(call: Any) -> None:
        """Handle the print_image service call."""
        image_path = call.data.get("image_path")

        await coordinator.print_image(image_path)

    hass.services.async_register(DOMAIN, "print_text", handle_print_text)
    hass.services.async_register(DOMAIN, "print_image", handle_print_image)
