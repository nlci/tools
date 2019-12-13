#!/usr/bin/python3

from fontParts.world import *
import sys

# Open UFO
ufo = sys.argv[1]
font = OpenFont(ufo)

# Query UFO

## List glyph names
for glyph in font:
    print(f'{glyph.name}')

# Modify UFO

# Save UFO
# font.changed()
# font.save()
# font.close()
