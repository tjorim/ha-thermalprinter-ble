# DingDang Printer - Home Assistant Integration

Home Assistant custom integration for DingDang label printers via Bluetooth.

## Features

- 🏠 **Native Home Assistant integration** - Seamless integration with HA
- 🔌 **Bluetooth discovery** - Automatic printer detection via Bluetooth
- 📝 **Print service** - Simple service to print text and images
- 🏷️ **Label templates** - Pre-defined templates for common labels
- 📊 **Sensor entities** - Monitor printer status, paper level, errors
- 🎨 **Lovelace card** - Custom card for easy printing from dashboard
- ⚙️ **Configuration UI** - Easy setup through the UI

## Installation

### HACS (Recommended)

1. Add this repository to HACS as a custom repository
2. Search for "DingDang Printer" in HACS
3. Click Install
4. Restart Home Assistant

### Manual Installation

1. Copy the `custom_components/dingdang_printer` folder to your `config/custom_components/` directory
2. Restart Home Assistant

## Setup

1. Go to **Settings** → **Devices & Services**
2. Click **+ Add Integration**
3. Search for "DingDang Printer"
4. Select your printer from the discovered devices
5. Follow the setup wizard

## Services

### `dingdang_printer.print_text`

Print text to the label printer.

```yaml
service: dingdang_printer.print_text
data:
  device_id: YOUR_DEVICE_ID
  text: "Hello World"
  font_size: 24
```

### `dingdang_printer.print_image`

Print an image from a file or URL.

```yaml
service: dingdang_printer.print_image
data:
  device_id: YOUR_DEVICE_ID
  image_path: "/config/www/qrcode.png"
```

### `dingdang_printer.print_template`

Print using a pre-defined template.

```yaml
service: dingdang_printer.print_template
data:
  device_id: YOUR_DEVICE_ID
  template: "package_label"
  variables:
    name: "John Doe"
    address: "123 Main St"
    tracking: "1Z999AA10123456789"
```

## Example Automations

### Print when door sensor opens

```yaml
automation:
  - alias: "Print visitor label"
    trigger:
      platform: state
      entity_id: binary_sensor.front_door
      to: "on"
    action:
      service: dingdang_printer.print_text
      data:
        device_id: YOUR_DEVICE_ID
        text: "Visitor at {{ now().strftime('%H:%M') }}"
```

### Print daily task list

```yaml
automation:
  - alias: "Morning task list"
    trigger:
      platform: time
      at: "08:00:00"
    action:
      service: dingdang_printer.print_template
      data:
        device_id: YOUR_DEVICE_ID
        template: "daily_tasks"
        variables:
          date: "{{ now().strftime('%Y-%m-%d') }}"
          tasks:
            - "Check emails"
            - "Morning standup"
            - "Review PRs"
```

### Print QR code for WiFi guests

```yaml
automation:
  - alias: "Print WiFi QR code"
    trigger:
      platform: event
      event_type: ios.action_fired
      event_data:
        actionName: PrintWiFiQR
    action:
      - service: python_script.generate_wifi_qr
        data:
          ssid: "Guest WiFi"
          password: "guest123"
      - service: dingdang_printer.print_image
        data:
          device_id: YOUR_DEVICE_ID
          image_path: "/config/www/wifi_qr.png"
```

## Sensors

The integration provides the following sensors:

- **Printer Status** - Current printer state (idle, printing, error)
- **Paper Level** - Paper status (ok, low, out)
- **Last Print** - Timestamp of last successful print
- **Error Status** - Current error state if any

## Configuration

Advanced configuration options:

```yaml
# configuration.yaml
dingdang_printer:
  default_font_size: 24
  default_density: 15
  paper_type: gap  # continuous, gap, or mark
  templates:
    package_label:
      width: 384
      height: 150
      fields:
        - name: name
          position: [10, 10]
          font_size: 28
        - name: address
          position: [10, 50]
          font_size: 20
        - name: tracking
          position: [10, 90]
          font_size: 16
          type: barcode
```

## Lovelace Card

Add the custom card to your dashboard:

```yaml
type: custom:dingdang-printer-card
entity: sensor.dingdang_printer_status
quick_prints:
  - text: "Test Label"
    icon: mdi:printer
  - text: "{{ now().strftime('%Y-%m-%d %H:%M') }}"
    icon: mdi:clock
```

## Troubleshooting

### Printer not discovered

1. Ensure Bluetooth is enabled in Home Assistant
2. Check that the printer is powered on and in range
3. Try restarting the Bluetooth integration
4. Check Home Assistant logs for errors

### Print quality issues

1. Adjust density in printer settings
2. Try different binarization methods
3. Ensure image resolution matches printer width (384px for 58mm)

### Connection issues

1. Only one device can connect to the printer at a time
2. Ensure the printer isn't connected to your phone/tablet
3. Try rebooting the printer
4. Check Bluetooth adapter compatibility

## Development

See [DEVELOPMENT.md](DEVELOPMENT.md) for contributing guidelines.

## License

MIT License - see LICENSE file

## Credits

Built on the [dingdang-printer](https://github.com/yourusername/dingdang-printer) Python library.
