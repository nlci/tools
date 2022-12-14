#!/usr/bin/python3

from fontParts.world import *
import sys

# Open UFO
ufo = sys.argv[1]
font = OpenFont(ufo)

# Query UFO

## Show glyph extents
for glyph in font:
    bounds = glyph.bounds
    if bounds is None:
        continue
    (xmin, ymin, xmax, ymax) = bounds
    print(f'glyph:{glyph.name} {ymin} {ymax}')

# Modify UFO

# Save UFO
# font.changed()
# font.save()
# font.close()
