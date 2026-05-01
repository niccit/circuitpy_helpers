# SPDX-License-Identifier: MIT


# If the battery is equal to or higher than 4.0 it's fully charged
def get_full_level():
    return 4.0

# If the battery is less than or equal to 3.9 and higher than 3.7 it's discharging
def get_discharging_level():
    high = 3.9
    low = 3.7
    return high, low

# If the battery is equal to or lower than 3.7 it is low and needs to be charged
def get_warning_level():
    return 3.7

# Return the raw output from the battery
# For battery monitor on boards like the Feather ESP32v2 Huzzah type -> v1
# For MAX17048 Battery Monitor OR LC709203F Battery Monitor type -> v2
def monitor_battery(battery, battery_type: str):
    voltage = None
    percentage = None
    if battery_type is "v1":
        voltage = battery.value
        voltage = voltage / 10000
    elif battery_type is "v2":
        voltage = round(battery.cell_voltage, 1)
        percentage = round(battery.cell_percent, 2)

    return voltage, percentage

# Return a pretty print version of voltage for logging/publishing
def format_battery_voltage(voltage):
    pretty_voltage = f"{voltage:0.2f}V"
    return pretty_voltage

# Return a pretty print version of percentage for logging/publishing
def format_battery_percentage(percentage):
    pretty_percentage = f"{percentage:0.2f}%"
    return pretty_percentage
