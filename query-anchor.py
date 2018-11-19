#!/usr/bin/python3

from fontParts.world import *
import sys

# Open UFO
ufo = sys.argv[1]
font = OpenFont(ufo)

# Query UFO

## Show anchor information
for glyph in font:
    for anchor in glyph.anchors:
        print(f'glyph: {glyph.name} ap: {anchor.name} x: {anchor.x}  y: {anchor.y}')

# Modify UFO

# Save UFO
# font.changed()
# font.save()
# font.close()
