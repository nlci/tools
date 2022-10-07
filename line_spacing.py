#!/usr/bin/python3

from fontParts.world import *
import sys

# Open UFO
ufo = sys.argv[1]
font = OpenFont(ufo)

# Line spacing metrics
# If there are two numbers for an expression, the second number is for a diacritic.
metrics = {
    # beng
    'Bhagirati': (-159, 881),

    # deva
    'Panini': (-665, 1384),
    'Kautilya': (-627, 1426),
    'Maurya': (-284, 747),

    # gujr
    'Gir': (-402, 801),

    # guru
    'Arjun': (-4, 659),

    # knda
    'Badami': (-326-200, 604),
    'Kaveri': (-316-200, 686),

    # mlym
    'Vayalar': (-3, 596),
    'Malabar': (-2, 600),
    'Bailey': (-1304, 1434),

    # orya
    'Asika': (-333, 804),

    # taml
    'ThiruValluvar': (-512-202, 1520+455),
    'Auvaiyar': (-342-99, 693+222),
    'Vaigai': (-250-99, 742+229),

    # telu
    'Nirmal': (-421, 625),
    'Asha': (-903, 1263),
    'Elur': (-903, 1521)
    }

metric = metrics[font.info.familyName]
descender, ascender = metric

# Modify UFO
font.info.ascender = ascender
font.info.descender = descender

font.info.openTypeOS2WinAscent = ascender
font.info.openTypeOS2WinDescent = -descender

font.info.openTypeOS2TypoAscender = ascender
font.info.openTypeOS2TypoDescender = descender
font.info.openTypeOS2TypoLineGap = 0

font.info.openTypeHheaAscender = ascender
font.info.openTypeHheaDescender = descender
font.info.openTypeHheaLineGap = 0

# Save UFO
font.changed()
font.save()
font.close()
