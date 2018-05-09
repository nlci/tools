#!/usr/bin/python3

from fontParts.world import *
import sys

# Open UFO
ufo = sys.argv[1]
font = OpenFont(ufo)

# Modify UFO
if font.info.xHeight is None:
    font.info.xHeight = 930
if font.info.capHeight is None:
    font.info.capHeight = 1500

# Save UFO
font.changed()
font.save()
font.close()
