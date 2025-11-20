# SPDX-License-Identifier: MIT
import random

import adafruit_led_animation.color

# Common methods that may be used across LED light projects

# Given a color name, return the tuple
# Uses for this include updating LED light configurations via MQTT
# Lazy way to not have to continually look up RGB codes
# While most of these return what's in the LED animation color library you can easily add more
def get_color_tuple(name):
    color = adafruit_led_animation.color.WHITE
    if name == "red":
        color = adafruit_led_animation.color.RED
    elif name == "yellow":
        color = adafruit_led_animation.color.YELLOW
    elif name == "orange":
        color = adafruit_led_animation.color.ORANGE
    elif name == "green":
        color = adafruit_led_animation.color.GREEN
    elif name == "teal":
        color = adafruit_led_animation.color.TEAL
    elif name == "cyan":
        color = adafruit_led_animation.color.CYAN
    elif name == "blue":
        color = adafruit_led_animation.color.BLUE
    elif name == "purple":
        color = adafruit_led_animation.color.PURPLE
    elif name == "magenta":
        color = adafruit_led_animation.color.MAGENTA
    elif name == "white":
        color = adafruit_led_animation.color.WHITE
    elif name == "black":
        color = adafruit_led_animation.color.BLACK
    elif name == "jade":
        color = adafruit_led_animation.color.JADE
    elif name == "pink":
        color = adafruit_led_animation.color.PINK
    elif name == "aqua":
        color = adafruit_led_animation.color.AQUA
    elif name == "gold":
        color = adafruit_led_animation.color.GOLD
    elif name == "amber":
        color = adafruit_led_animation.color.AMBER
    elif name == "old_lace":
        color = adafruit_led_animation.color.OLD_LACE
    elif name == "indigo":
        color = (75,0,130)
    elif name == "chocolate":
        color = (210,105,30)
    return color

# Generate a random coloGr
# Excludes black and white
# Returns a tuple
def get_random_color():
    red = random.randrange(190, 200)
    green = random.randrange(190, 200)
    blue = random.randrange(190, 200)
    random_color = (red, green, blue)
    return random_color

# Pre-defined color palettes to use across applications
# Returns a list of tuples
def get_color_palette(name):
    palette = []
    if name == "rainbow":
        palette = adafruit_led_animation.color.RAINBOW
    elif name == "christmas":
        palette = (adafruit_led_animation.color.RED, adafruit_led_animation.color.GREEN, adafruit_led_animation.color.YELLOW, adafruit_led_animation.color.BLUE)
    elif name == "fall":
        palette = (adafruit_led_animation.color.ORANGE, adafruit_led_animation.color.RED, adafruit_led_animation.color.GOLD, adafruit_led_animation.color.YELLOW)
    return palette



