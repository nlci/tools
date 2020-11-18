#!/usr/bin/python3

from fontParts.world import *
import sys

# Open UFO
ufo = sys.argv[1]
font = OpenFont(ufo)

# Modify UFO

## ensure curves are in the correct direction
for glyph in font:
    glyph.correctDirection()

# Save UFO
font.changed()
font.save()
font.close()
