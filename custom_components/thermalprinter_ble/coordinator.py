"""DataUpdateCoordinator for Thermal Printer."""
from __future__ import annotations

from datetime import timedelta
import logging
from typing import Any

from bleak.backends.device import BLEDevice
from thermalprinter_ble import BLEDevice as ThermalBLEDevice, ThermalPrinter, PrinterStatus
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .const import DEFAULT_SCAN_INTERVAL, DOMAIN

_LOGGER = logging.getLogger(__name__)


class ThermalPrinterDataUpdateCoordinator(DataUpdateCoordinator[PrinterStatus]):
    """Class to manage fetching thermal printer data."""

    def __init__(self, hass: HomeAssistant, ble_device: BLEDevice) -> None:
        """Initialize coordinator."""
        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=timedelta(seconds=DEFAULT_SCAN_INTERVAL),
        )
        self.ble_device = ble_device
        self._device: ThermalBLEDevice | None = None
        self._printer: ThermalPrinter | None = None

    async def _async_update_data(self) -> PrinterStatus:
        """Fetch data from printer."""
        try:
            if self._printer is None:
                await self._async_setup()

            # Get printer status
            status = await self._printer.get_status()  # type: ignore
            return status

        except Exception as err:
            _LOGGER.error("Error communicating with printer: %s", err)
            raise UpdateFailed(f"Error communicating with printer: {err}") from err

    async def _async_setup(self) -> None:
        """Set up the printer connection."""
        try:
            self._device = ThermalBLEDevice(self.ble_device.address)
            self._printer = ThermalPrinter(self._device)
            await self._printer.initialize()
            _LOGGER.info("Connected to thermal printer: %s", self.ble_device.address)
        except Exception as err:
            _LOGGER.error("Failed to connect to printer: %s", err)
            raise

    async def print_text(self, text: str, font_size: int = 24) -> None:
        """Print text to the printer."""
        if self._printer is None:
            await self._async_setup()

        try:
            await self._printer.print_text(text, font_size)  # type: ignore
            await self._printer.finish_print()  # type: ignore
            _LOGGER.info("Printed text: %s", text)
        except Exception as err:
            _LOGGER.error("Failed to print text: %s", err)
            raise

    async def print_image(self, image_path: str) -> None:
        """Print an image to the printer."""
        if self._printer is None:
            await self._async_setup()

        try:
            await self._printer.print_image(image_path)  # type: ignore
            await self._printer.finish_print()  # type: ignore
            _LOGGER.info("Printed image: %s", image_path)
        except Exception as err:
            _LOGGER.error("Failed to print image: %s", err)
            raise

    async def async_shutdown(self) -> None:
        """Shutdown the coordinator."""
        if self._printer:
            await self._printer.close()
            self._printer = None
            self._device = None
