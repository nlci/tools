#!/usr/bin/python3

from fontParts.world import *
import sys

# Open UFO
ufo = sys.argv[1]
font = OpenFont(ufo)

# Line spacing metrics
metrics = {
    # beng
    'Bhagirati': (-1012, 2152), # from taml, needs to be adjusted

    # deva
    'Panini': (-1012, 2152), # from taml, needs to be adjusted
    'Kautilya': (-1012, 2152), # from taml, needs to be adjusted
    'Maurya': (-1012, 2152), # from taml, needs to be adjusted

    # gujr
    'Gir': (-1012, 2152), # from taml, needs to be adjusted

    # guru
    'Arjun': (-1012, 2152), # from taml, needs to be adjusted

    # knda
    'KAN Badami': (-1012, 2152), # from taml, needs to be adjusted
    'KAN Kaveri': (-1012, 2152), # from taml, needs to be adjusted

    # taml
    'ThiruValluvar': (-1012, 2152), # v0.271 had (-1029, 2650)
    'Auvaiyar': (-494, 1042),
    'Vaigai': (-494, 1057),

    # telu
    'Nirmal': (-1012, 2152), # from taml, needs to be adjusted
    'Asha': (-1012, 2152), # from taml, needs to be adjusted
    'Elur': (-1012, 2152) # from taml, needs to be adjusted
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
