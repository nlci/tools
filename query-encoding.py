#!/usr/bin/python3

from fontParts.world import *
import sys

# Open UFO
ufo = sys.argv[1]
font = OpenFont(ufo)

# Query UFO

## Check if the first three glyphs exist
otspec = ('.notdef', '.null', 'nonmarkingreturn')
for first_glyphs in otspec:
    if first_glyphs not in font:
        print(f'glyph {first_glyphs} is not in the font')

## Find glyphs with encoding issues
cmap = dict()
for glyph in font:

    # Only check encoded glyphs
    if len(glyph.unicodes) == 0:
        continue

    # Check for a USV used by another glyph
    if glyph.unicode in cmap:
        print(f'glyph {glyph.name} has USV of U+{glyph.unicode:04X}, but that USV is also used for glyph {cmap[glyph.unicode]}')

    # Add codepoint of current glyph
    cmap[glyph.unicode] = glyph.name

    # Ensure glyph names match encoding (for names starting with u or uni)
    name = None
    if glyph.name.startswith('uni'):
        name = glyph.name[3:]
    elif glyph.name.startswith('u'):
        name = glyph.name[1:]
    try:
        usv = int(name, 16)
        if usv != glyph.unicode:
            print(f'glyph {glyph.name} has incorrect USV of U+{glyph.unicode:04X}')
    except:
        pass

    # Ligatures should not be encoded
    if '.' in glyph.name or '_' in glyph.name:
        print(f'glyph {glyph.name} is a ligature but has an encoding of U+{glyph.unicode:04X}')

    # Ensure the same USV is specified
    if glyph.unicode != glyph.unicodes[0]:
        print(f'glyph {glyph.name} has inconsistent encodings')

    # Check for double encoding (one glyph has multiple USVs)
    if len(glyph.unicodes) > 1:
        print(f'glyph {glyph.name} has multiple encodings')

# Modify UFO

# Save UFO
# font.changed()
# font.save()
# font.close()
