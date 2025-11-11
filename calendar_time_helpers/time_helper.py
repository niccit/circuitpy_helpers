# SPDX-License-Identifier: MIT

from datetime import datetime

# Return the current minute and the current_time
# Example use for current_min - know when to update a time display
def get_current_time():
    now = datetime.now()
    current_min = now.minute
    current_time = now.strftime("%H:%M")
    return current_min, current_time


