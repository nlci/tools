#!/usr/bin/python3

from fontParts.world import *
import sys

# Open UFO
ufo = sys.argv[1]
font = OpenFont(ufo)

# Latin mappings
latins = {
    # For deva, a Latin font has not been selected

    # deva
    'Panini': 'gentium',
    'Kautilya': 'gentium',
    'Maurya': 'gentium',

    # knda
    'KAN Badami': 'gentium',
    'KAN Kaveri': 'exo',

    # taml
    'ThiruValluvar': 'gentium',
    'Auvaiyar': 'charis',
    'Vaigai': 'gentium'
    }

xheights = {
    'charis': 987,
    'gentium': 930,
    'exo': 1096
    }

capheights = {
    'charis': 1374,
    'gentium': 1260,
    'exo': 1509
    }

latin = latins[font.info.familyName]
xheight = xheights[latin]
capheight = capheights[latin]

# Modify UFO
if font.info.xHeight is None:
    font.info.xHeight = xheight
if font.info.capHeight is None:
    font.info.capHeight = capheight

# Save UFO
font.changed()
font.save()
font.close()
