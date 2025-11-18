# SPDX-License-Identifier: MIT

import time

# Return the current minute and the current_time
# Example use for current_min - know when to update a time display
# This is for a board that has a system clock, i.e., Raspberrypi
def get_current_time():
    from datetime import datetime
    now = datetime.now()
    current_min = now.minute
    current_time = now.strftime("%H:%M")
    return current_min, current_time


# Will properly format a UNIX timestamp into a readable value
def format_time(timestamp):
    local_time = time.localtime(timestamp)
    return "{:02d}:{:02d}:{:02d}".format(local_time.tm_hour, local_time.tm_min, local_time.tm_sec)

# Will return the UNIX time
def get_unix_time():
    from datetime import datetime
    from datetime import timezone
    return datetime.now(tz=timezone.utc).isoformat()

# Given a timestamp, will take the hour and minute and convert it to seconds
def get_time_in_seconds(timestamp):
    hour, minute = timestamp.split(':')
    hour_in_seconds = int(hour)* 3600
    minute_in_seconds = int(minute)* 60
    time_in_seconds = hour_in_seconds + minute_in_seconds

    return time_in_seconds

def convert_stringtime_to_time(timestamp):
    hour, minute = timestamp.split(':')
    new_time = time.struct_time([int(hour), int(minute)])
    return new_time