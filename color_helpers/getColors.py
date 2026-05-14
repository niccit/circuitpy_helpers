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
    elif name == "light yellow":
        color = (255,255,224)
    elif name == "mint cream":
        color = (245,255,250)
    elif name == "lavender":
        color = (230,230,250)
    elif name == "ghost white":
        color = (248,248,255)
    elif name == "light sky blue":
        color = (135,206,250)
    elif name == "papaya whip":
        color = (255,239,213)
    elif name == "snow":
        color = (255,250,250)
    return color

# Generate a random coloGr
# Excludes black and white
# Returns a tuple
def get_random_color():
    red = random.randrange(0, 7) * 32
    green = random.randrange(0, 7) * 32
    blue = random.randrange(0, 7) * 32
    random_color = (red, green, blue)
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
        palette = (adafruit_led_animation.color.AQUA, adafruit_led_animation.color.TEAL, (127,255,212), (32,178,170), (60,179,113))
    elif name == "palelight":
        palette = (get_color_tuple("light yellow"), get_color_tuple("light sky blue"), get_color_tuple("papaya whip"), get_color_tuple("lavender"),  get_color_tuple("mint cream"))
    elif name == "whites":
        palette = (get_color_tuple("old_lace"), get_color_tuple("snow"), get_color_tuple("ghost white"))
    return palette



