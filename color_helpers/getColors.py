# SPDX-License-Identifier: MIT
import random

import adafruit_led_animation.color

# Common methods that may be used across LED light projects

# Given a color name, return the tuple
# Uses for this include updating LED light configurations via MQTT
# Lazy way to not have to continually look up RGB codes
# While most of these return what's in the LED animation color library you can easily add more
def get_color_tuple(name):
    color = adafruit_led_animation.color.PINK
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
    elif name == "dark turquoise":
        color = (0,206,209)
    return color

# Generate a random coloGr
# Excludes black and white
# Returns a tuple
def get_random_color():
    random_color = tuple(random.choices(range(256), k=3))
    return random_color

# Pre-defined color palettes to use across applications
# Returns a list of tuples
def get_color_palette(name):
    palette = adafruit_led_animation.color.RAINBOW
    if name == "rainbow":
        palette = adafruit_led_animation.color.RAINBOW
    elif name == "christmas":
        palette = (adafruit_led_animation.color.RED, adafruit_led_animation.color.GREEN, adafruit_led_animation.color.YELLOW, adafruit_led_animation.color.BLUE)
    elif name == "fall":
        palette = (adafruit_led_animation.color.ORANGE, adafruit_led_animation.color.RED, adafruit_led_animation.color.GOLD, adafruit_led_animation.color.YELLOW)
    elif name == "hanukkah":
        palette = (adafruit_led_animation.color.BLUE, (240, 240, 240))
    elif name == "halloween":
        palette = ((247,95,28),(255,154,0), (136,30,228), (133,226,31))
    elif name == "patrick":
        palette = ((34,77,23), (9,148,65), (96,168,48), (159,218,64), (217,233,29))
    elif name == "valentine":
        palette = ((94,8,30), (181,26,58), (226,71,103), (228,131,151), (228,205,211))
    elif name == "easter":
        palette = ((255,212,229), (224,205,255), (189,232,239), (183,215,132), (254,244,162))
    elif name == "fourth":
        palette = ((30,24,96), (196,31,64), (240, 240, 240))
    elif name == "blues":
        palette = (adafruit_led_animation.color.BLUE, (24, 24, 112), (0, 0, 128), (65,105,255), (245, 24, 112))
    elif name == "purples":
        palette = (adafruit_led_animation.color.PURPLE, adafruit_led_animation.color.MAGENTA, (218,112,214), (153,50,204))
    elif name == "sea":
        palette = (adafruit_led_animation.color.AQUA, adafruit_led_animation.color.TEAL, (127,255,212), (32,178,170), (60, 179.113))
    return palette



