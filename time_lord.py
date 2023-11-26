# SPDX-License-Identifier: MIT

import time
import adafruit_ntp
import local_logger as logger

try:
    from data import data
except ImportError:
    print("Timezone data is stored in data.py. Please create the file")
    raise


# The time singleton
# No value until configured
time_lord = None


# Configure the time singleton
def configure_time(socket_pool, rtc):
    _add_time_lord(socket_pool, rtc)
    return time_lord


# Private method to create time singleton, if one is not already created
def _add_time_lord(socketpool, rtc):
    global time_lord

    if time_lord is None:
        time_lord = TimeLord(socketpool, rtc)
        time_lord.set_system_clock()
        message = "Created Time Singleton"
        time_lord.my_log.log_message(message, "info")


# Return the configured time singleton
# Returns nothing if configure_time() hasn't already been called
def get_time_lord():
    if time_lord is not None:
        return time_lord
    else:
        print("time singleton not configured!")
        raise RuntimeError


class TimeLord:

    # Initialize the time singleton
    def __init__(self, socketpool, rtc):
        self.rtc = rtc
        self.socket_pool = socketpool
        self.my_log = logger.getLocalLogger()

    # Set up NTP client
    # get the current datetime and set the RTC
    def set_system_clock(self):

        ntp_client = adafruit_ntp.NTP(self.socket_pool, tz_offset=float(data["tz_offset"]))
        attempt = 0
        connect_success = False

        while connect_success is False:
            try:
                self.rtc.datetime = ntp_client.datetime
                connect_success = True
            except OSError as oe:
                if attempt <= 5:
                    message = "failed to connect to NTP, retrying ..."
                    self.my_log.log_message(message, "warning")
                    attempt += 1
                    time.sleep(2)
                    pass
                else:
                    message = "Tried " + str(attempt) + "times, could not connect to NTP: " + str(oe)
                    self.my_log.log_message(message, "critical")
                    raise RuntimeError

    # Return the current date/time for logging
    # Formatted: Y.D.M HH:MM:SS
    def get_logging_datetime(self):
        now = self.rtc.datetime
        t = "{:02d}.{:02d}.{:02d} {:02d}:{:02d}:{:02d}".format(now.tm_year, now.tm_mday, now.tm_mon, now.tm_hour,
                                                               now.tm_min, now.tm_sec)
        return t

    # Return the current date
    # Formatted: YDM
    def get_date(self, separator=None):
        now = self.rtc.datetime
        if separator is not None:
            d = "{:02d}" + separator + "{:02d}" + separator + "{:02d}".format(now.tm_year, now.tm_mday, now.tm_mon)
        else:
            d = "{:02d}{:02d}{:02d}".format(now.tm_year, now.tm_mday, now.tm_mon)

        return d

    # Return the current time with seconds
    # Formatted: HH:MM:SS
    def get_time_seconds(self):
        now = self.rtc.datetime
        t = "{:02d}:{:02d}:{:02d}".format(now.tm_hour, now.tm_min, now.tm_sec)
        return t

    # Return the current time without seconds
    # Formatted: HH:MM
    def get_time(self):
        now = self.rtc.datetime
        t = "{:02d}:{:02d}".format(now.tm_hour, now.tm_min)
        return t

    # Returns current datetime from the RTC
    # This method returns as a time.struct_time
    # Format (tm_year, tm_mon, tm_mday, tm_hour, tm_min, tm_sec, tm_wday, tm_yday, tm_isdst)
    def get_current_time(self):
        return self.rtc.datetime
