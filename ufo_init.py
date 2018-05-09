#!/usr/bin/python3

from fontParts.world import *
import sys

# Open UFO
ufo = sys.argv[1]
font = OpenFont(ufo)

# Latin mappings
latins = {
    'KAN Badami': 'gentium',
    'KAN Kaveri': 'exo'
    }

xheights = {
    'gentium': 930,
    'exo': 1096
    }

capheights = {
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
