# SPDX-License-Identifier: MIT
import supervisor
import os

# common methods that may be used across different projects


# Defaults to data.py
# Provides for on the fly backup and restoration of a given file
# Use explicit path to file when calling method
# Example use: temporarily updating configurations using MQTT
def backup_and_restore(filename="data.py", backup=False, restore=False):
    backup_filename = filename + "_bu"
    if restore:
        try:
            os.rename(backup_filename, filename)
            supervisor.reload()
        except OSError as e:
            print(f"Could not restore configuration file {backup_filename}, does not exist")
            pass

    if backup:
        try:
            file = open(filename, "r")
            contents = file.read()
            file.close()
            file = open(backup_filename, "w")
            file.write(contents)
            file.close()
            dir_list = os.listdir("/")
        except OSError as e:
            print(f"Could not backup configuration file {filename}, does not exist")
            pass
import json

# Purpose: Update a data.py file on the fly
# Input: JSON format or MQTT message
# Expected Format:
#   filename: <file to modify>
#   search_string: <what is to be replaced>
#   new_value: <what you want it to be>
#   example: "filename": "data.py", "search_string": "['rainbow_sparkle', 'rainbow_comet']", "new_value": "['cycle']"
# Tips:
#   remain consistent with the structure of your file
#   be certain you have the exact string, replace can be unforgiving
#   be sure your new value is properly formatted
# Handles:
#   Numbers
#   Lists
#   Plain strings
# update_data_file performs an inline replacement of the old value with the new value
# Default for replace count is 1, it can be modified
# WARNING: this is destructive - it will overwrite your file
def update_data_file(message, search_name, count=1):
    in_data = json.loads(message)
    filename = in_data["filename"]
    search_string = in_data["search_string"]
    updated_value = in_data["new_value"]
    try:
        if float(in_data["search_string"]):
            search_string = "'" + search_name + "'" + ": " + str(in_data["search_string"])
            updated_value = "'" + search_name + "'" + ": " + str(in_data["new_value"])
    except ValueError:
        if "[" in in_data["search_string"]:
            search_string = "'" + search_name + "'" + ": " + str(in_data["search_string"])
            updated_value = "'" + search_name + "'" + ": " + "[" + str(in_data["new_value"]) + "]"
        else:
            search_string = "'" + search_name + "'" + ": " + "'" + str(in_data["search_string"]) + "'"
            updated_value = "'" + search_name + "'" + ": " + str(in_data["new_value"])
        pass

    try:
        with open(filename, 'r') as file:
            file_data = file.read()
            if search_name in file_data:
                updated_content = file_data.replace(search_string, updated_value, count)
        file.close()
    except FileNotFoundError:
        print(f"Could read from {filename}, does not exist")
        pass
    try:
        with open(filename, 'w') as file:
            file.write(updated_content)
        file.close()
    except FileNotFoundError:
        print(f"Could write to {filename}, does not exist")
        pass
