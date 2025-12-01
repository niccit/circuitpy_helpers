# SPDX-License-Identifier: MIT
import alarm
from alarm import time
import time
import supervisor

# Common methods that may be used across projects

# Check if lights should be put to sleep until scheduled time
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
# Returns True or False
def check_need_shutdown(now_time, stop_time, start_time, sleep_time, before_start_time):
    running_time = (now_time - start_time)
    time_diff = (sleep_time - running_time) - before_start_time
    if stop_time != 0:
        if now_time >= stop_time and time_diff > 0:
            check = True
        else:
            check = False
        return check
    else:
        return False

# Put lights to sleep until scheduled start time
# supervisor.reload() is there because lights freeze when coming out of sleep without it
def sleep_before_set_time(now_time, set_time, before_set_time):
    time_diff = (set_time - now_time) - before_set_time
    wake_alarm = alarm.time.TimeAlarm(monotonic_time=time.monotonic() + time_diff)
    alarm.light_sleep_until_alarms(wake_alarm)
    supervisor.reload()

# Put lights to sleep for specified amount of time - sleep_time
# supervisor.reload() is there because lights freeze when coming out of sleep without it
def shutdown(now_time, stop_time, start_time, sleep_time, before_start_time, pixels):
    running_time = (now_time - start_time)
    time_diff = (sleep_time - running_time) - before_start_time
    wake_alarm = alarm.time.TimeAlarm(monotonic_time=time.monotonic() + time_diff)
    alarm.light_sleep_until_alarms(wake_alarm)
    supervisor.reload()

# Call method if pixels should be blanked for any reason
# i.e., sleeping before a specified time or for a specified period of time
def blank_all(pixels):
    pixels.fill((0, 0, 0))
    pixels.show()