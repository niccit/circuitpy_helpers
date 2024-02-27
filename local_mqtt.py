# SPDX-License-Identifier: MIT


import ssl
import adafruit_minimqtt.adafruit_minimqtt as my_mqtt
from adafruit_io.adafruit_io import IO_MQTT
import local_logger as logger

mqtt_prime = None  # The only MQTT client, we don't need multiple


# Create or retrieve a MQTT object by name; only retrieves MQTT objects created using this function.
# There can only be one MQTT object; if one already exists it will be returned
# Requires the socketpool name in order to fullyl set up the MQTT client
def getMqtt(use_logger: bool = False):
    _addMqtt(use_logger)
    return mqtt_prime


def _addMqtt(use_logger):
    global mqtt_prime

    if mqtt_prime is None:
        mqtt_prime = MessageBroker(use_logger)


# All the data we need to set up mqtt_client
try:
    from mqtt_data import mqtt_data
except ImportError:
    log_message = "MQTT data stored in mqtt_data.py, please create file"
    print(log_message)
    raise


# Return properly formatted topic
def get_formatted_topic(feed_name):
    if mqtt_data["is_adafruit_io"] is True:
        return mqtt_data["username"] + "/feeds/" + feed_name + "/json"
    else:
        return feed_name


# The class where the mqtt_client is initialized
class MessageBroker:

    # Initialize the mqtt_client
    # This method should never be called directly, use getMqtt() instead
    def __init__(self, use_logger):
        self.mqtt_client = my_mqtt.MQTT(
            broker=mqtt_data["server"],
            port=mqtt_data["port"],
            username=mqtt_data["username"],
            password=mqtt_data["key"],
            is_ssl=mqtt_data["use_ssl"],
            ssl_context=ssl.create_default_context(),
        )
        self.io = None
        self.gen_feed = mqtt_data["primary_feed"]
        if mqtt_data["is_adafruit_io"] is True:
            self.gen_topic = mqtt_data["username"] + "/feeds/" + self.gen_feed + "/json"
        else:
            self.gen_topic = self.gen_feed
        self.use_logger = use_logger
        if self.use_logger is True:
            self.my_log = logger.getLocalLogger()

    # --- Getters --- #

    # Return self.io
    # If it is none that MQTT is not fully configured
    def get_io(self):
        return self.io

    # --- Methods --- #

    # Configure MQTT to use socketpool
    def configure_publish(self, pool_name, iface=None):
        if iface is not None:
            my_mqtt.set_socket(pool_name, iface)
        else:
            my_mqtt.set_socket(pool_name)
        self.io = IO_MQTT(self.mqtt_client)

    # Connect to the MQTT broker
    def connect(self):
        if not self.mqtt_client.is_connected():
            if mqtt_data["is_adafruit_io"] is True:
                self.io.connect()
            else:
                self.mqtt_client.connect()

    # Subscribe to MQTT topics
    def subscribe(self, topics):
        for t in range(len(topics)):
            topic = get_formatted_topic(topics[t])
            self.mqtt_client.subscribe(topic)

    # Publish to MQTT
    def publish(self, topic, io_message, log_level: str = "notset", sdcard_dump: bool = False):

        if self.use_logger is True:
            self.my_log.add_mqtt_stream(topic)
            try:
                if sdcard_dump is True:
                    self.my_log.log_message(io_message, log_level, mqtt=True, sdcard_dump=True)
                else:
                    self.my_log.log_message(io_message, log_level, mqtt=True)
            except OSError as oe:
                message = "Unable to publish to MQTT! " + str(oe)
                print(message)
                pass
        else:
            print(log_level, " - ", io_message)
            self.mqtt_client.publish(topic, io_message)
