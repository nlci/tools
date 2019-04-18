#!/usr/bin/python3

from fontParts.world import *
import sys

# Open UFO
ufo = sys.argv[1]
font = OpenFont(ufo)

# Query UFO

## Show anchor information
# anchors = set()
for glyph in font:
    # bounds = glyph.bounds
    # if bounds is None:
    #     continue
    # (left, bottom, right, top) = bounds
    for anchor in glyph.anchors:
        print(f'glyph: {glyph.name} ap: {anchor.name} x: {anchor.x}  y: {anchor.y}')
        # if glyph.unicode is None:
        #     codepoint = 0
        # else:
        #     codepoint = glyph.unicode
        # print(f'glyph: {codepoint:05X} {glyph.name} ap: {anchor.name} x: {anchor.x}  y: {anchor.y}')
        # if anchor.name == 'U':
        #     space = anchor.y - top
        #     print(f'glyph: {glyph.name} {top} + {space} = {anchor.y}')
        # anchors.add(anchor.name)
# print(anchors)

# Modify UFO

# Save UFO
# font.changed()
# font.save()
# font.close()
