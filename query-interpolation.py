#!/usr/bin/python3

from fontParts.world import *
import sys

# Open UFOs
ufo1 = sys.argv[1]
font1 = OpenFont(ufo1)

ufo2 = sys.argv[2]
font2 = OpenFont(ufo2)

# Query UFO

## Are the glyph inventories the same
inventory1 = set()
for glyph in font1:
    inventory1.add(glyph.name)

inventory2 = set()
for glyph in font2:
    inventory2.add(glyph.name)

print('glyphs only in font 1')
for glyph_name in sorted(inventory1 - inventory2):
    print(glyph_name)

print('glyphs only in font 2')
for glyph_name in sorted(inventory2 - inventory1):
    print(glyph_name)

## Are glyphs compatible for interpolation
for glyph_name in inventory1 & inventory2:
    glyph1 = font1[glyph_name]
    glyph2 = font2[glyph_name]
    compatible, report = glyph1.isCompatible(glyph2)
    if not compatible:
        print(f'glyph {glyph_name} is not compatible for interpolation\n{str(report)}')

# Modify UFO

# Save UFO
# font.changed()
# font.save()
# font.close()
