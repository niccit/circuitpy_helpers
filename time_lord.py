# SPDX-License-Identifier: MIT

# Wrapper class for setting and getting time information
# Currently does not support portal boards using Network

import time
import adafruit_ntp
from rtc import RTC

import local_logger as logger
import local_mqtt

try:
    from data import data
except ImportError:
    print("Timezone data is stored in data.py. Please create the file")
    raise


# The time singleton
# No value until configured
time_lord = None
# Get whether to use adafruit_logger from the data file
use_log = data["local_logger"]


# Configure the time singleton
# If not using a real time clock, pass in any value for rtc
# rtc will only get used if it is of type RTC
def configure_time(socket_pool, rtc):
    _add_time_lord(socket_pool, rtc)
    return time_lord


# Private method to create time singleton, if one is not already created
def _add_time_lord(socketpool, rtc):
    global time_lord

    if time_lord is None:
        time_lord = TimeLord(socketpool, rtc)
        if use_log == 1:
            time_lord.my_log = logger.getLocalLogger()
        if time_lord.rtc is not None:
            time_lord.set_system_clock()
        else:
            time_lord.print_message("Time Singleton Created", "info")


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
        if type(rtc) is not RTC:
            self.rtc = None
        else:
            self.rtc = rtc
        self.socket_pool = socketpool
        self.my_log = None
        self.ntp_client = adafruit_ntp.NTP(self.socket_pool, tz_offset=float(data["tz_offset"]))

    # Set up NTP client
    # get the current datetime and set the RTC
    def set_system_clock(self):

        attempt = 0
        connect_success = False

        while connect_success is False:
            try:
                self.rtc.datetime = self.ntp_client.datetime
                connect_success = True
                message = "Created Time Singleton and updated RTC"
                self.print_message(message, "info")
            except OSError as oe:
                if attempt <= 5:
                    message = "failed to connect to NTP, retrying ..."
                    self.print_message(message, "warning")
                    attempt += 1
                    time.sleep(2)
                    pass
                else:
                    message = "Tried " + str(attempt) + "times, could not connect to NTP: " + str(oe)
                    self.print_message(message, "critical")
                    raise RuntimeError

    # Return the current date/time for logging
    # Formatted: Y.D.M HH:MM:SS
    def get_logging_datetime(self):
        now = self._provide_time_data()
        t = "{:02d}.{:02d}.{:02d} {:02d}:{:02d}:{:02d}".format(now.tm_year, now.tm_mday, now.tm_mon, now.tm_hour,
                                                               now.tm_min, now.tm_sec)
        return t

    # Return the current date
    # Formatted: YDM
    def get_date(self, separator=None):
        now = self._provide_time_data()
        if separator is not None:
            d = "{:02d}" + separator + "{:02d}" + separator + "{:02d}".format(now.tm_year, now.tm_mday, now.tm_mon)
        else:
            d = "{:02d}.{:02d}.{:02d}".format(now.tm_year, now.tm_mday, now.tm_mon)

        return d

    # Return the current time with seconds
    # Formatted: HH:MM:SS
    def get_time_seconds(self):
        now = self._provide_time_data()
        t = "{:02d}:{:02d}:{:02d}".format(now.tm_hour, now.tm_min, now.tm_sec)
        return t

    # Return the current time without seconds
    # Formatted: HH:MM
    def get_time(self):
        now = self._provide_time_data()
        t = "{:02d}:{:02d}".format(now.tm_hour, now.tm_min)
        return t

    # Roll your own datetime format!
    # This method returns as a time.struct_time
    #       Format (tm_year, tm_mon, tm_mday, tm_hour, tm_min, tm_sec, tm_wday, tm_yday, tm_isdst)
    # Use this method if you don't want the default date display of YYYY.DD.MM
    def get_current_time(self):
        return self._provide_time_data()

    def _provide_time_data(self):
        if self.rtc is None:
            return self.ntp_client.datetime
        else:
            return self.rtc.datetime

    # In order to be flexible and not create a dependency between time_lord and local_logger
    # Handle print statements accordingly
    def print_message(self, message, level, sdcard_dump: bool = False):
        if use_log == 1:
            self.my_log.log_message(message, level, sdcard_dump=sdcard_dump)
        else:
            print(message)
