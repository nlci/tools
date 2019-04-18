#!/usr/bin/python3

from fontParts.world import *
import sys

# Open UFO
ufo = sys.argv[2]
font = OpenFont(ufo)

# Modify UFO
mode = sys.argv[1]
k = 'keep'
for glyph in font:
    for anchor in glyph.anchors:
        if mode == 'mark':
            anchor.name += k
        elif mode == 'only':
            if anchor.name.endswith(k):
                anchor.name = anchor.name.replace(k, '')
            else:
                glyph.removeAnchor(anchor)

# Save UFO
font.changed()
font.save()
font.close()
