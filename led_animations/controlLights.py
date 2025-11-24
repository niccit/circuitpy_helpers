# SPDX-License-Identifier: MIT
import alarm
import time
import supervisor

# Common methods that may be used across projects

# If start up time is before sunset, sleep until set_time
def sleep_before_set_time(now_time, set_time, before_set_time, ignore_sunset, pixels):
    if now_time < set_time:
        time_diff = (set_time - now_time) - before_set_time
        if 0 < time_diff <= set_time and not ignore_sunset:
            wake_alarm = alarm.time.TimeAlarm(monotonic_time=time.monotonic() + time_diff)
            _blank_all(pixels)
            alarm.light_sleep_until_alarms(wake_alarm)
            supervisor.reload()

# If up and running, and it's shut off time, sleep until next day around set_time
def shutdown(now_time, stop_time, start_time, sleep_time, before_start_time, pixels):
    running_time = (now_time - start_time)
    time_diff = (sleep_time - running_time) - before_start_time
    if now_time >= stop_time and time_diff > 0:
        wake_alarm = alarm.time.TimeAlarm(monotonic_time=time.monotonic() + time_diff)
        _blank_all(pixels)
        alarm.light_sleep_until_alarms(wake_alarm)
        supervisor.reload()

def _blank_all(pixels):
   pixels.fill((0, 0, 0))
   pixels.show()