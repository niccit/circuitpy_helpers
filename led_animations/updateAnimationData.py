# SPDX-License-Identifier: MIT

from circuitpy_helpers.color_helpers import getColors

# This file will assist with common replacements specific to LED lighting
# It can handle overriding pre-set values for animations
# As well as changing colors and the active animation

# Use this to override default settings for animations, in animations.json
def override_default_settings(data_file, possible_overrides, item):
    override_array = possible_overrides
    for o in override_array:
        name = item['name'] + "_" + o + "_override"
        try:
            if data_file[name] is not None:
                item[o] = data_file[name]
        except KeyError:
            pass

    return item

# Set the color based on what's specified in json file
# If sending an array of colors, animation must support it
# Supports random color, list of colors, color palette, single color
def set_color(data_file, item):
    try:
        if "random" in item['colors']:
            color = getColors.get_random_color()
            item['colors'] = color
        elif "data" in item['colors']:
            color_list = []
            name = item['name'] + "_color"
            colors = data_file[name]
            if type(colors) == list:
                for color in colors:
                    choice = getColors.get_color_tuple(color)
                    color_list.append(choice)
                item['colors'] = color_list
            elif "palette" in colors:
                header, palette = colors.split("_")
                color_list = getColors.get_color_palette(palette)
                item['colors'] = color_list
            elif "None" in colors:
                item['colors'] = getColors.get_color_tuple('indigo')
            else:
                choice = getColors.get_color_tuple(colors)
                item['colors'] = choice
    except KeyError:
        pass

    return item

