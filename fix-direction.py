#!/usr/bin/python3

from fontParts.world import *
import sys

# Open UFO
ufo = sys.argv[1]
font = OpenFont(ufo)

glyph_name = sys.argv[2]

# Modify UFO

## ensure curves are in the correct direction
glyph = font[glyph_name]
glyph.correctDirection()

# Save UFO
font.changed()
font.save()
font.close()
