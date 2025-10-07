# Copilot Instructions for Thermal Printer (BLE)

This repository contains a Home Assistant custom integration for DingDang thermal label printers that connect via Bluetooth Low Energy (BLE).

## Project Overview

This is a Home Assistant custom component that enables:
- Automatic discovery of thermal printers via Bluetooth
- Printing text and images to 58mm thermal label printers
- Monitoring printer status through sensor entities
- Service calls for printing operations

## Architecture

### Component Structure
```
custom_components/thermalprinter_ble/
├── __init__.py          # Integration setup and service registration
├── config_flow.py       # Configuration flow for UI setup
├── const.py            # Constants and configuration values
├── coordinator.py      # DataUpdateCoordinator for printer communication
├── sensor.py           # Sensor entities for status monitoring
├── manifest.json       # Integration metadata
├── services.yaml       # Service definitions
└── strings.json        # UI strings for configuration
```

### Key Components

1. **Config Flow** (`config_flow.py`)
   - Handles Bluetooth device discovery
   - Supports both automatic discovery and manual selection
   - Uses Home Assistant's Bluetooth integration

2. **Coordinator** (`coordinator.py`)
   - Manages BLE connection to printer
   - Implements `DataUpdateCoordinator` for data fetching
   - Handles print operations (text and images)
   - Monitors printer status

3. **Sensors** (`sensor.py`)
   - Status sensor (idle, printing, error, offline)
   - Error sensor for error messages
   - Uses coordinator for data updates

4. **Services** (`__init__.py`)
   - `thermalprinter_ble.print_text` - Print text with font size
   - `thermalprinter_ble.print_image` - Print images from file path

## Code Style and Conventions

### Home Assistant Integration Guidelines

1. **Follow Home Assistant Core Standards**
   - Use type hints for all functions and methods
   - Use `async`/`await` for all I/O operations
   - Follow Home Assistant's entity naming conventions
   - Implement proper error handling with `ConfigEntryNotReady`, `UpdateFailed`, etc.

2. **Code Organization**
   - One platform per file (sensor.py, etc.)
   - Keep coordinator logic separate from entity logic
   - Use constants from `const.py` for magic values

3. **Logging**
   - Use module-level logger: `_LOGGER = logging.getLogger(__name__)`
   - Log important state changes at INFO level
   - Log errors with context at ERROR level
   - Avoid logging sensitive data (MAC addresses should be sanitized if needed)

4. **Error Handling**
   - Use `ConfigEntryNotReady` for setup failures that should retry
   - Use `UpdateFailed` in coordinator for temporary communication failures
   - Always include error context in exception messages

### Python Style

- Follow PEP 8 and Home Assistant's style guide
- Use double quotes for strings
- Keep functions focused and single-purpose
- Use descriptive variable names (avoid abbreviations except common ones like `hass`)

### Type Annotations

```python
# Always use type hints
async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up from config entry."""
    
# Use Union or | for multiple types (Python 3.10+)
def example(value: str | None = None) -> dict[str, Any]:
    """Example function."""
```

## Bluetooth Integration

### Device Discovery

- Integration filters for devices with name containing "DingDang" or specific service UUID
- Uses Home Assistant's `bluetooth` component for discovery
- Implements `async_step_bluetooth` for automatic discovery
- Implements `async_step_user` for manual device selection

### BLE Communication

- Uses `thermalprinter-ble` Python library for printer communication
- Library provides `ThermalBLEDevice` and `ThermalPrinter` classes
- Connection is initialized in coordinator's `_async_setup` method
- Proper cleanup in `async_shutdown` method

## Development Workflow

### Making Changes

1. **Testing Changes**
   - This is a Home Assistant integration, best tested in a live HA environment
   - Use Home Assistant's developer tools to test services
   - Check the logs for errors: Settings → System → Logs
   - Use the Integration's reload to test changes without restarting HA

2. **Adding Features**
   - New sensors: Add to `SENSOR_TYPES` in `sensor.py`
   - New services: Register in `async_setup_services()` in `__init__.py`
   - Update `services.yaml` and `strings.json` for UI descriptions

3. **Configuration Changes**
   - Update `manifest.json` for version, requirements, or Bluetooth filters
   - Update `hacs.json` for HACS-related changes

### Dependencies

- Requires `thermalprinter-ble==0.1.0` Python library
- Built on Home Assistant's Bluetooth integration
- Minimum Home Assistant version: 2023.9.0

## Domain-Specific Knowledge

### Thermal Printers

- **58mm thermal printers** - Standard label printer width (384px)
- **Paper types**: continuous, gap (with gaps between labels), mark (black mark detection)
- **Density**: Print darkness setting (typically 0-31, default 15)
- **Font sizes**: Typically 16-48px for legibility on small labels

### Printer Status

The printer status is obtained through the `PrinterStatus` class from the library:
- `is_idle`: True when ready to print
- `has_error`: True when error condition exists
- `has_data`: True when actively printing

### Common Operations

1. **Print Text**
   ```python
   await coordinator.print_text("Hello World", font_size=24)
   ```

2. **Print Image**
   ```python
   await coordinator.print_image("/path/to/image.png")
   ```

3. **Get Status**
   ```python
   status = await printer.get_status()
   ```

## Testing

Currently, there is no automated test infrastructure in this repository. Testing should be done manually:

1. Install in a test Home Assistant instance
2. Test discovery and configuration
3. Test printing operations via services
4. Verify sensor states update correctly
5. Test error handling (disconnect printer, etc.)

## Common Patterns

### Adding a New Sensor

1. Add description to `SENSOR_TYPES` tuple in `sensor.py`:
   ```python
   SensorEntityDescription(
       key="paper_level",
       name="Paper Level",
       icon="mdi:printer-pos-alert",
   ),
   ```

2. Update `native_value` property to handle new sensor type:
   ```python
   elif self.entity_description.key == "paper_level":
       return status.paper_level if hasattr(status, 'paper_level') else "unknown"
   ```

### Adding a New Service

1. Define handler in `async_setup_services()` in `__init__.py`:
   ```python
   async def handle_new_service(call: Any) -> None:
       """Handle service call."""
       # Service logic here
   ```

2. Register service:
   ```python
   hass.services.async_register(DOMAIN, "service_name", handle_new_service)
   ```

3. Add service definition to `services.yaml`

## Important Notes

- **Single connection**: Only one device can connect to the printer at a time
- **Range**: Bluetooth range is limited (typically 10m/30ft)
- **Compatibility**: Integration designed for DingDang brand printers but may work with compatible models
- **Image requirements**: Images should be properly sized for printer width (384px for 58mm)

## Getting Help

- Check Home Assistant logs for detailed error messages
- Verify Bluetooth is working in Home Assistant
- Ensure printer is powered on and in range
- Only one device should be connected to printer at a time

## Future Enhancements

Potential areas for improvement:
- Add configuration options for default print settings
- Implement label template system
- Add paper level detection (if hardware supports)
- Support for different printer models
- QR code and barcode generation services
- Custom Lovelace card for quick printing
