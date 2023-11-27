# SPDX-License-Identifier: MIT


import ssl
import adafruit_minimqtt.adafruit_minimqtt as my_mqtt
from adafruit_io.adafruit_io import IO_MQTT
import local_logger as logger

mqtt_prime = None  # The only MQTT client, we don't need multiple

# Get logging level
try:
    from data import data
except ImportError:
    print("Logging level stored in data.py, please create file")
    raise

use_log = data["local_logger"]


# Create or retrieve a MQTT object by name; only retrieves MQTT objects created using this function.
# There can only be one MQTT object; if one already exists it will be returned
# Requires the socketpool name in order to fullyl set up the MQTT client
def getMqtt():
    _addMqtt()
    return mqtt_prime


def _addMqtt():
    global mqtt_prime

    if mqtt_prime is None:
        mqtt_prime = MessageBroker()
        message = "Created MQTT singleton"
        mqtt_prime.print_message(message, "info")


# Return properly formatted topic
def get_formatted_topic(feed_name):
    return mqtt_data["username"] + "/feeds/" + feed_name + "/json"


# All the data we need to set up mqtt_client
try:
    from mqtt_data import mqtt_data
except ImportError:
    log_message = "MQTT data stored in mqtt_data.py, please create file"
    print(log_message, "critical")
    raise


# The class where the mqtt_client is initialized
class MessageBroker:

    # Initialize the mqtt_client
    # This method should never be called directly, use getMqtt() instead
    def __init__(self):
        self.mqtt_client = my_mqtt.MQTT(
            broker=mqtt_data["server"],
            port=mqtt_data["port"],
            username=mqtt_data["username"],
            password=mqtt_data["key"],
            is_ssl=True,
            ssl_context=ssl.create_default_context()
        )
        self.io = None
        self.gen_feed = mqtt_data["primary_feed"]
        self.gen_topic = mqtt_data["username"] + "/feeds/" + self.gen_feed + "/json"
        if use_log == 1:
            self.my_log = logger.getLocalLogger()

    # --- Getters --- #

    # Return self.io
    # If it is none that MQTT is not fully configured
    def get_io(self):
        return self.io

    # --- Methods --- #

    # Configure MQTT to use socketpool
    def configure_publish(self, pool_name):
        my_mqtt.set_socket(pool_name)
        self.io = IO_MQTT(self.mqtt_client)

    # Connect to the MQTT broker
    def connect(self):
        if not self.mqtt_client.is_connected():
            self.io.connect()

    # Subscribe to MQTT topics
    def subscribe(self, topics):
        for t in range(len(topics)):
            topic = mqtt_data["username"] + "/feeds/" + topics[t]
            self.mqtt_client.subscribe(topic)

    # Publish to MQTT
    def publish(self, topic, io_message, log_level: str = "notset", sdcard_dump: bool = False):

        if not self.mqtt_client.is_connected():
            message = "Need to connect to MQTT"
            self.print_message(message, "info")
            self.connect()

        if use_log == 1:
            try:
                self.my_log.add_mqtt_stream(topic)
                if sdcard_dump is True:
                    self.print_message(io_message, log_level, mqtt=True, sdcard_dump=True)
                else:
                    self.print_message(io_message, log_level, mqtt=True)
            except OSError as oe:
                message = "Unable to publish to MQTT! " + str(oe)
                self.print_message(message, "critical")
                pass
        else:
            self.print_message("Publishing to MQTT")
            self.mqtt_client.publish(topic, io_message)

    # In order to be flexible and not create a dependency between time_lord and local_logger
    # Handle print statements accordingly
    def print_message(self, message, level: str = "debug", mqtt: bool = False, sdcard_dump: bool = False):
        if use_log == 1:
            self.my_log.log_message(message, level, mqtt, sdcard_dump)
        else:
            print(message)
