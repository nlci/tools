#!/usr/bin/python3

from fontParts.world import *
import sys

# Open UFO
ufo = sys.argv[1]
font = OpenFont(ufo)

# Modify UFO

## Decompose all glyphs
for glyph in font:
    glyph.decompose()

# Save UFO
font.changed()
font.save()
font.close()
