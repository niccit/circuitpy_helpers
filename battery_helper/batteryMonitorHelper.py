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
def monitor_battery(battery):
    voltage = round(battery.cell_voltage, 1)
    percentage = round(battery.cell_percent, 2)
    return voltage, percentage


# Return a pretty print version of voltage and percentage for logging/publishing
def format_battery_data(voltage, percentage):
    pretty_voltage = f"{voltage:0.2f}"
    pretty_percentage = f"{percentage:0.2f}"
    return pretty_voltage, pretty_percentage