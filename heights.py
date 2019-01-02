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

    # orya
    'Asika': 'sophia_nubian1000',

    # taml
    'ThiruValluvar': 'gentium2048',
    'Auvaiyar': 'charis1000',
    'Vaigai': 'gentium1000',

    # telu
    'Nirmal': 'gentium1000',
    'Asha': 'gentium2048',
    'Elur': 'sophia_nubian2048'
    }

workshops = {
    # taml
    'ThiruValluvar': 0.9,
    'Auvaiyar': 0.9,
    'Vaigai': 0.9
    }

xheights = {
    'charis2048': 987,
    'charis1000': 987 * 1000/2048,
    'gentium2048': 930,
    'gentium1000': 930 * 1000/2048,
    'sophia_nubian1000': 500,
    'sophia_nubian2048': 500 * 2048/1000,
    'exo1000': 536
    }

capheights = {
    'charis2048': 1374,
    'charis1000': 1374 * 1000/2048,
    'gentium2048': 1260,
    'gentium1000': 1260 * 1000/2048,
    'sophia_nubian1000': 722,
    'sophia_nubian2048': 722 * 2048/1000,
    'exo1000': 738
    }

family = font.info.familyName
latin = latins[family]
workshop = workshops.get(family, 1/1.4)
xheight = round(xheights[latin] * workshop)
capheight = round(capheights[latin] * workshop)

# Modify UFO
font.info.xHeight = xheight
font.info.capHeight = capheight

# Save UFO
font.changed()
font.save()
font.close()
