#!/usr/bin/python3

from fontParts.world import *
import sys

def collect(filename):
    font = OpenFont(filename)
    inventory = set()
    cmap = set()
    for glyph in font:
        inventory.add(glyph.name)
        if glyph.unicode is not None:
            cmap.add(glyph.unicode)
    return font, inventory, cmap

# Open UFOs
font1, inventory1, cmap1 = collect(sys.argv[1])
font2, inventory2, cmap2 = collect(sys.argv[2])

## Are the glyph inventories the same
print('glyphs only in font 1')
for glyph_name in sorted(inventory1 - inventory2):
    print(glyph_name)

print('glyphs only in font 2')
for glyph_name in sorted(inventory2 - inventory1):
    print(glyph_name)

## Are the codepoints the same
print('codepoints only in font 1')
for codepoint in sorted(cmap1 - cmap2):
    print(f'{codepoint:04X}')

print('codepoints only in font 2')
for codepoint in sorted(cmap2 - cmap1):
    print(f'{codepoint:04X}')

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
