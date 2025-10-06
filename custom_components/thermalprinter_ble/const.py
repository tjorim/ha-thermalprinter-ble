"""Constants for the Thermal Printer (BLE) integration."""

DOMAIN = "thermalprinter_ble"

# Configuration
CONF_PAPER_TYPE = "paper_type"
CONF_DENSITY = "density"
CONF_FONT_SIZE = "font_size"

# Defaults
DEFAULT_FONT_SIZE = 24
DEFAULT_DENSITY = 15
DEFAULT_SCAN_INTERVAL = 30  # seconds

# Paper types
PAPER_TYPE_CONTINUOUS = "continuous"
PAPER_TYPE_GAP = "gap"
PAPER_TYPE_MARK = "mark"

# Printer states
STATE_IDLE = "idle"
STATE_PRINTING = "printing"
STATE_ERROR = "error"
STATE_OFFLINE = "offline"
