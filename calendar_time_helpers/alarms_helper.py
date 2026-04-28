# SPDX-License-Identifier: MIT

import alarm
from alarm import time
import time
import supervisor

# Time Alarms

# Check if project should invoke sleep until a specific time
# Generally used at start up of project only
# Returns True or False
def check_need_sleep(now_time, set_time, before_set_time, ignore_sleep_time):
    if now_time < set_time:
        time_diff = (set_time - now_time) - before_set_time
        if 0 < time_diff <= set_time and not ignore_sleep_time:
            check = True
        else:
            check = False
        return check
    else:
        return False

# Check if lights should be put to sleep for a specified amount of time; i.e. next day
# After project is up and running this would invoke periods of sleep based on schedule
# Returns True or False
def check_need_shutdown(now_time, start_time, before_start_time, ignore_shutdown_time):
    if now_time > start_time:
        time_diff = (start_time - now_time) - before_start_time
        if 0 < time_diff <= start_time and not ignore_shutdown_time:
            check = True
        else:
            check = False
        return check
    else:
        return False

# Put lights to sleep until scheduled start time
# supervisor.reload() is there because lights freeze when coming out of light sleep without it
# Sleep type: 0 -> light sleep, 1 -> deep sleep
def sleep_before_set_time(now_time, set_time, before_set_time, sleep_type=0):
    time_diff = (set_time - now_time) - before_set_time
    wake_alarm = alarm.time.TimeAlarm(monotonic_time=time.monotonic() + time_diff)
    if sleep_type == 1:
        alarm.exit_and_deep_sleep_until_alarms(wake_alarm)
    else:
        alarm.light_sleep_until_alarms(wake_alarm)
        supervisor.reload()

# Put lights to sleep until specified wake time i.e., sunrise
# supervisor.reload() is there because lights freeze when coming out of light sleep without it
# Sleep type: 0 -> light sleep, 1 -> deep sleep
def shutdown(now_time, start_time, before_start_time, sleep_type=0 ):
    time_diff = (start_time - now_time) - before_start_time
    wake_alarm = alarm.time.TimeAlarm(monotonic_time=time.monotonic() + time_diff)
    if sleep_type == 1:
        alarm.exit_and_deep_sleep_until_alarms(wake_alarm)
    else:
        alarm.light_sleep_until_alarms(wake_alarm)
        supervisor.reload()
