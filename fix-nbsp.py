#!/usr/bin/python3

from fontParts.world import *
import sys

# Open UFO
ufo = sys.argv[1]
font = OpenFont(ufo)

# Modify UFO

## Make NBSP the same width as a normal space

# Find the needed space glyphs
for glyph in font:
    if glyph.unicode:
        if glyph.unicode == 0x0020:
            space = glyph
        if glyph.unicode == 0x00A0:
            nbsp = glyph

# Set width of NBSP correctly
nbsp.width = space.width

# Save UFO
font.changed()
font.save()
font.close()
