# SPDX-License-Identifier: MIT

from datetime import datetime
from datetime import timezone
import time

# Return the current minute and the current_time
# Example use for current_min - know when to update a time display
# This is for a board that has a system clock, i.e., Raspberrypi
def get_current_time():
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
    return datetime.now(tz=timezone.utc).isoformat()