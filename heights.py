#!/usr/bin/python3

from fontParts.world import *
import sys

# Open UFO
ufo = sys.argv[1]
font = OpenFont(ufo)

# Latin mappings
latins = {
    # For deva, a Latin font has not been selected

    # beng
    'Bhagirati': 'gentium1000',

    # deva
    'Panini': 'gentium2048',
    'Kautilya': 'gentium2048',
    'Maurya': 'gentium1000',

    # knda
    'KAN Badami': 'gentium1000',
    'KAN Kaveri': 'exo1000',

    # taml
    'ThiruValluvar': 'gentium2048',
    'Auvaiyar': 'charis1000',
    'Vaigai': 'gentium1000'
    }

xheights = {
    'charis2048': 987,
    'charis1000': round(987 * 1000/2048),
    'gentium2048': 930,
    'gentium1000': round(930 * 1000/2048),
    'exo1000': 536
    }

capheights = {
    'charis2048': 1374,
    'charis1000': round(1374 * 1000/2048),
    'gentium2048': 1260,
    'gentium1000': round(1260 * 1000/2048),
    'exo1000': 738
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
