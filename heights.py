#!/usr/bin/python3

from fontParts.world import *
import sys

# Open UFO
ufo = sys.argv[1]
font = OpenFont(ufo)

# Latin mappings
latins = {
    # beng
    'Bhagirati': 'gentium1000',

    # deva
    'Panini': 'charis2048',
    'Kautilya': 'charis2048',
    'Maurya': 'charis1000',

    # gujr
    'Gir': 'charis1000',

    # guru
    'Arjun': 'sophia_nubian1000',

    # knda
    'Badami': 'gentium1000',
    'Kaveri': 'exo1000',

    # taml
    'ThiruValluvar': 'gentium2048',
    'Auvaiyar': 'charis1000',
    'Vaigai': 'gentium1000',

    # telu
    'Nirmal': 'gentium1000',
    'Asha': 'gentium2048',
    'Elur': 'sophia_nubian2048'
    }

xheights = {
    'charis2048': 987,
    'charis1000': round(987 * 1000/2048),
    'gentium2048': 930,
    'gentium1000': round(930 * 1000/2048),
    'sophia_nubian1000': 500,
    'sophia_nubian2048': round(500 * 2048/1000),
    'exo1000': 536
    }

capheights = {
    'charis2048': 1374,
    'charis1000': round(1374 * 1000/2048),
    'gentium2048': 1260,
    'gentium1000': round(1260 * 1000/2048),
    'sophia_nubian1000': 722,
    'sophia_nubian2048': round(722 * 2048/1000),
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
