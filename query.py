#!/usr/bin/python3

from fontParts.world import *
import sys

# Open UFO
ufo = sys.argv[1]
font = OpenFont(ufo)

# Query UFO

# Make sure we only have one layer
print(f'{font.defaultLayerName} (default)') # could also be font.defaultLayer.name
for layer in font.layers:
    print(f'{layer.name} (layer)')

# taml
for glyph in font:
    for anchor in glyph.anchors:
        if anchor.name == 'N':
            pass
            # print('y:{} {} {}'.format(anchor.y, glyph.name, anchor.name))

# Modify UFO

# Save UFO
# font.changed()
# font.save()
# font.close()