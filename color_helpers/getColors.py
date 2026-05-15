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
    elif name == "crimson":
        color = (220,20,60)
    elif name == "tomato":
        color = (255,99,71)
    elif name == "indian red":
        color = (205,92,92)
    elif name == "light coral":
        color = (240, 128, 128)
    elif name == "salmon":
        color = (250,128,114)
    elif name == "orange":
        color = adafruit_led_animation.color.ORANGE
    elif name == "papaya whip":
        color = (255, 239, 213)
    elif name == "coral":
        color = (255, 127, 80)
    elif name == "gold":
        color = adafruit_led_animation.color.GOLD
    elif name == "goldenrod":
        color = (218,165,32)
    elif name == "pale goldenrod":
        color = (238,232,170)
    elif name == "pink":
        color = adafruit_led_animation.color.PINK
    elif name == "sea shell":
        color = (255, 245, 238)
    elif name == "light pink":
        color = (255,182,193)
    elif name == "magenta":
        color = adafruit_led_animation.color.MAGENTA
    elif name == "violet":
        color = (238,130,238)
    elif name == "deep pink":
        color = (255,20,147)
    elif name == "yellow":
        color = adafruit_led_animation.color.YELLOW
    elif name == "light yellow":
        color = (255, 255, 224)
    elif name == "amber":
        color = adafruit_led_animation.color.AMBER
    elif name == "green":
        color = adafruit_led_animation.color.GREEN
    elif name == "teal":
        color = adafruit_led_animation.color.TEAL
    elif name == "jade":
        color = adafruit_led_animation.color.JADE
    elif name == "dark turquoise":
        color = (0, 206, 209)
    elif name == "pale green":
        color = (152,251,152)
    elif name == "light green":
        color = (144,238,144)
    elif name == "blue":
        color = adafruit_led_animation.color.BLUE
    elif name == "cyan":
        color = adafruit_led_animation.color.CYAN
    elif name == "aqua":
        color = adafruit_led_animation.color.AQUA
    elif name == "light sky blue":
        color = (135, 206, 250)
    elif name == "alice blue":
        color = (240, 248, 255)
    elif name == "azure":
        color = (240, 255, 255)
    elif name == "sky blue":
        color = (135, 206, 235)
    elif name == "light blue":
        color = (173, 216, 230)
    elif name == "purple":
        color = adafruit_led_animation.color.PURPLE
    elif name == "indigo":
        color = (75, 0, 130)
    elif name == "lavender":
        color = (230, 230, 250)
    elif name == "blue violet":
        color = (138,43,226)
    elif name == "dark orchid":
        color = (153,50,204)
    elif name == "plum":
        color = (221,160,221)
    elif name == "orchid":
        color = (218,112,214)
    elif name == "white":
        color = adafruit_led_animation.color.WHITE
    elif name == "old_lace":
        color = adafruit_led_animation.color.OLD_LACE
    elif name == "ghost white":
        color = (248, 248, 255)
    elif name == "snow":
        color = (255, 250, 250)
    elif name == "black":
        color = adafruit_led_animation.color.BLACK
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
        palette = (adafruit_led_animation.color.BLUE, adafruit_led_animation.color.WHITE)
    elif name == "halloween":
        palette = (get_color_tuple("indigo"), adafruit_led_animation.color.ORANGE, adafruit_led_animation.color.GOLD, adafruit_led_animation.color.GREEN)
    elif name == "patrick":
        palette = (adafruit_led_animation.color.GREEN, adafruit_led_animation.color.TEAL, adafruit_led_animation.color.JADE, get_color_tuple("light green"))
    elif name == "valentine":
        palette = (adafruit_led_animation.color.PINK, get_color_tuple("light pink"), get_color_tuple("deep pink"), get_color_tuple("violet"))
    elif name == "easter":
        palette = (get_color_tuple("light pink"), get_color_tuple("light green"), get_color_tuple("light blue"), get_color_tuple("light yellow"))
    elif name == "fourth":
        palette = (adafruit_led_animation.color.RED, adafruit_led_animation.color.WHITE, adafruit_led_animation.color.BLUE)
    elif name == "blues":
        palette = (adafruit_led_animation.color.BLUE, get_color_tuple("light sky blue"), get_color_tuple("alice blue"))
    elif name == "purples":
        palette = (adafruit_led_animation.color.PURPLE, get_color_tuple("indigo"), get_color_tuple("dark orchid"), get_color_tuple("plum"))
    elif name == "sea":
        palette = (adafruit_led_animation.color.AQUA, adafruit_led_animation.color.TEAL, get_color_tuple("azure"), get_color_tuple("dark turquoise"), adafruit_led_animation.color.JADE)
    elif name == "lights":
        palette = (get_color_tuple("light yellow"), get_color_tuple("light sky blue"), get_color_tuple("papaya whip"), get_color_tuple("lavender"),  get_color_tuple("mint cream"))
    elif name == "whites":
        palette = (get_color_tuple("old_lace"), get_color_tuple("snow"), get_color_tuple("ghost white"), get_color_tuple("sea shell"))
    return palette



