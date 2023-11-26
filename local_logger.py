# SPDX-License-Identifier: MIT

# A wrapper to adafruit_logging that allows multiple class files to access and act on a single logger
# Objective is to simplify adding Handlers

import json
import os
import time
import adafruit_logging as a_logger
from adafruit_logging import FileHandler, NOTSET, Handler, LogRecord
import time_lord
# import one_mqtt


main_log = None
handlers = []


# Create or return the logger this project uses
# If the local logger does not exist it will be created
# For this project the local logger is console
def getLocalLogger():
    _addLocalLogger()
    return main_log


try:
    from data import data
except ImportError:
    print("Logging information stored in data.py, please create file")
    raise


def _addLocalLogger():
    global main_log

    if main_log is None:
        main_log = LocalLogger()
        main_log.add_console_stream()
        message = "Created local logger"
        main_log.log_message(message, "info")


# Take in a string and return the proper logging level
# Needed so that consumers of the class don't need to send in the proper log level format - string or int
def get_log_level(level: str = "notset"):
    if level is "debug":
        return a_logger.DEBUG
    elif level is "info":
        return a_logger.INFO
    elif level is "warning":
        return a_logger.WARNING
    elif level is "error":
        return a_logger.ERROR
    elif level is "critical":
        return a_logger.CRITICAL
    else:
        return a_logger.NOTSET


# The wrapper - this creates the singleton logging object
# Methods for adding, closing, and removing handlers provided
# A simple log_message method is provided
class LocalLogger:

    # Initialize the wrapper
    # This should never be called directly, use getLocalLogger() instead
    def __init__(self):
        self._the_log = a_logger.getLogger('console')
        self._the_log.setLevel(data["log_level"])
        self.file_handler = None
        self.mqtt_handler = None
        self.my_time = time_lord.get_time_lord()

    # Logging to an SD card
    def add_sd_stream(self):
        if self.file_handler not in handlers:
            try:
                log_name = data["sd_logfile"]
                log_filepath = "/sd/" + log_name
                self.file_handler = FileHandler(log_filepath)
                self._the_log.addHandler(self.file_handler)
                handlers.append(self.file_handler)
            except OSError as oe:
                self._the_log.log(get_log_level("warning"), "unable to add sd stream " + str(oe))

    # Flush the file_handler stream to SD
    def flush_sd_stream(self):
        if self.file_handler in handlers:
            try:
                self.file_handler.stream.flush()
            except OSError as oe:
                message = "could not flush FileHandler to disk, SD card may be corrupted! " + str(oe)
                self._the_log.log(get_log_level("error"), message)
                pass

    # Close the sd card handler and remove it from the logger
    def close_sd_stream(self):
        if self._the_log.hasHandlers():
            if self.file_handler in handlers:
                self.file_handler.close()  # This performs: stream.flush and stream.close
                self._the_log.removeHandler(self.file_handler)
                handlers.remove(self.file_handler)

    # General console logging
    def add_console_stream(self):
        stream_handler = a_logger.StreamHandler()
        self._the_log.addHandler(stream_handler)

    # Logging to an MQTT broker
    def add_mqtt_stream(self, topic):
        if self.mqtt_handler not in handlers:
            my_mqtt = one_mqtt.getMqtt()
            self.mqtt_handler = MQTTHandler(my_mqtt.mqtt_client, topic)
            self._the_log.addHandler(self.mqtt_handler)
            handlers.append(self.mqtt_handler)

    # Remove the MQTT stream from the logger
    def remove_mqtt_stream(self):
        if self._the_log.hasHandlers():
            if self.mqtt_handler in handlers:
                self._the_log.removeHandler(self.mqtt_handler)
                handlers.remove(self.mqtt_handler)

    # Log a message to all relevant handlers
    # If using MQTT we need to handle if we're sending logging data or JSON data
    # Passing in True for the mqtt attribute will tell this method that it is JSON data
    # If notset is passed with mqtt then the level will be set to info; this is so things don't crash
    def log_message(self, message, level: str = "notset", mqtt: bool = False, sdcard_dump: bool = False):

        if mqtt is True:
            if level is "notset" or sdcard_dump is True:
                level = "info"
                io_message = message
            else:
                log_info = level.upper()
                io_message = log_info + " - " + self.my_time.get_logging_datetime() + ": " + message

            try:
                self._the_log.log(get_log_level(level), json.dumps(io_message))
            except OSError as oe:
                message = "MQTT logging failed, " + str(oe)
                self._the_log.log(get_log_level("error"), message)
                pass
        else:
            try:
                self._the_log.log(get_log_level(level), self.my_time.get_logging_datetime() + ": " + message)
            except OSError as oe:
                message = "Console/SD logging failed, " + str(oe)
                self._the_log.log(get_log_level("error"), message)
                pass

        # Remove MQTT handler
        if self.mqtt_handler in handlers:
            self._the_log.removeHandler(self.mqtt_handler)
            handlers.remove(self.mqtt_handler)

        # Write to the SD card file
        if self.file_handler in handlers:
            self.flush_sd_stream()

    # --- Methods to interact with the SD card without having to remove it --- #
    # Output specified number of lines of log file to disk
    # If restart is True then exclude the most recent 13 lines (start up messages)
    def dump_sd_log(self, logfile, lines_to_read, restart: bool = False):

        # If not logfile provided, print message and get out of dodge
        if logfile is None:
            self.log_message("No logfile specified!", "error")
            return

        self.close_sd_stream()

        list_of_log_levels = ["DEBUG", "INFO", "WARNING", "CRITICAL", "ERROR"]
        file = "/sd/" + logfile
        num = lines_to_read
        log_length = 0
        start_read = 0

        # Try to read the log file
        # If unable just log an error and move on
        try:
            with open(file, 'r') as logfile:
                log_output = logfile.readlines()
            logfile.close()
            log_length = len(log_output)
            start_read = log_length - num
        except OSError:
            self.log_message("unable to open and read syslog file", "warning")
            pass

        # Decide if we need to start reading the file prior to the initial 13 start up lines
        if log_length != 0:
            if restart is True:
                on_start_lines = 13
                if log_length > on_start_lines:
                    end_read = log_length - on_start_lines
                    start_read = end_read - num
                    new_log_output = log_output[start_read:end_read]
                else:
                    new_log_output = log_output[start_read:log_length]
            else:
                new_log_output = log_output[start_read:log_length]

            # Read the selected content and remove all " and carriage returns
            # If we don't the output will look hideous
            self.log_message("log file output is " + str(len(new_log_output)) + " long ", "debug")
            for line in range(len(new_log_output)):
                string = _get_split_string(new_log_output[line])
                self.log_message("string is " + str(len(string)) + " long and is " + str(string), "debug")

                # Assign new_string based on length of string
                if len(string) > 1:
                    new_string = string[1]
                else:
                    new_string = string

                # If any logging level is in the string, use this array to remove it
                strip_level = [sub for sub in list_of_log_levels if sub in new_string]
                if len(strip_level) > 0:
                    remove_string = strip_level[0] + " - "
                    self.log_message("remove string is " + str(remove_string), "debug")
                    # Remove all log levels in string
                    new_string = new_string.replace(remove_string, '')

                # Remove all double quotes in string
                new_string = new_string.replace('"', '')

                mqtt = one_mqtt.getMqtt()
                self.add_mqtt_stream(mqtt.gen_topic)
                self.log_message("LOG: " + new_string.strip('\r\n'), "info", mqtt=True, sdcard_dump=True)
                time.sleep(0.25)
                self.add_mqtt_stream(mqtt.gen_topic)

            self.add_sd_stream()
            self.log_message("End read sdcard log file", "info", mqtt=True)

    # Read and return the contents of a file
    def read_file(self, filename):

        # If not logfile provided, print message and get out of dodge
        if filename is None:
            self.log_message("No file provided!")
            return

        output = []
        try:
            file = "/sd/" + filename
            mqtt = one_mqtt.getMqtt()
            self.add_mqtt_stream(mqtt.gen_topic)
            with open(file, 'r') as file:
                output.append(file.readlines())
            file.close()
            return output
        except OSError:
            self.log_message("unable to open and read " + str(filename), "warning")
            pass

    # List the directories on the SD card where we store log and state files
    # Just a sanity check in case something goes wonky
    def list_sd_card(self, directory):
        if directory is None:
            list_dir = "/sd/"
        else:
            list_dir = "/sd/" + directory

        self.log_message("Request to list SD card contents for directory: " + str(directory), "info")
        try:
            os.listdir(list_dir)
            mqtt = one_mqtt.getMqtt()
            self.add_mqtt_stream(mqtt.gen_topic)
            self.log_message(str(directory) + ": " + str(os.listdir(list_dir)), "info", mqtt=True)
        except OSError:
            self.log_message("Unable to list directory " + str(directory), "warning")
            pass

    # Maintenance, rotate the system log on a monthly basis
    def rotate_sd_log(self, logfile):
        if logfile is None:
            self.log_message("No logfile provided!")
            return

        file = "/sd/" + logfile
        rotate_file = file + "." + self.my_time.get_data()
        os.rename(file, rotate_file)


# Class to handle publishing to the MQTT broker
class MQTTHandler(Handler):
    def __init__(self, mqtt_client: MQTT.MQTT, topic: str) -> None:
        super().__init__()

        self._mqtt_client = mqtt_client
        self._topic = topic

        self.level = NOTSET

    def emit(self, record: LogRecord) -> None:
        try:
            if self._mqtt_client.is_connected():
                self._mqtt_client.publish(self._topic, record.msg)
        except RuntimeError:
            pass

    def handle(self, record: LogRecord) -> None:
        self.emit(record)


# --- Private Methods --- #

# split string on log level and return result
def _get_split_string(log_line):
    if " DEBUG - " in log_line:
        return log_line.rsplit(" DEBUG - ")
    elif " INFO - " in log_line:
        return log_line.rsplit(" INFO - ")
    elif " WARNING - " in log_line:
        return log_line.rsplit(" WARNING - ")
    elif " ERROR - " in log_line:
        return log_line.rsplit(" ERROR - ")
    elif " CRITICAL - " in log_line:
        return log_line.rsplit(" CRITICAL - ")
    else:
        return log_line
