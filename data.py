# Add these three key/value pairs to your data file and set the ones you want to use to 1
# time_lord - a wrapper to time that provides formatted date/timestamps and will set the RTC if your board has one,
#    works with FeatherWings, and other external board providing RTC
# local_logger - a wrapper to adafruit_logging that forces your app to use one logger
#    provides methods to add FileHandler and MQTT streams and manage those streams
# local_mqtt - a wrapper to adafruit_minimqtt that forces your app to use one MQTT broker
#    provides methods to publish, subscribe, and configure
#    handles both direct publishing to MQTT as well as via the MQTTHandler in adafruit_logging
# Each wrapper works independently as well as alongside other wrappers
# 0 = No
# 1 = Yes

data = {
    'time_lord': 0,
    'local_logger': 0,
    'local_mqtt': 0,
}