#!/usr/bin/python3

from fontParts.world import *
import json
import sys

# Open UFO
ufo = sys.argv[3]
font = OpenFont(ufo)

# Modify UFO
mode = sys.argv[1]
k = 'keep'
with open(sys.argv[2]) as latin_anchor_file:
    latin_anchors = json.load(latin_anchor_file)
for glyph in font:
    for anchor in glyph.anchors:
        if mode == 'mark':
            anchor.name += k
        elif mode == 'only':
            if anchor.name.endswith(k):
                anchor.name = anchor.name.replace(k, '')
            elif anchor.name in latin_anchors['mark']:
                # Latin combing diacritics
                continue
            elif anchor.name in latin_anchors['base']: # and glyph.unicode is not None and glyph.unicode < 0x300:
                # Latin base characters
                continue
            else:
                glyph.removeAnchor(anchor)

# Save UFO
font.changed()
font.save()
font.close()
