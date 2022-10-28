#!/usr/bin/python3

from fontParts.world import *
import sys

# Open UFO
ufo = sys.argv[1]
font = OpenFont(ufo)

# Modify UFO

# Find the suffix used for the Indic specific punctuation
script_code = ''
for glyph in font:
    glyph_name = glyph.name
    if glyph_name.startswith('hyphen.'):
        script_code = glyph_name.split('.')[1]

# list of glyph names of Indic specific punctuation
glyph_names = list()
for glyph in font:
    glyph_name = glyph.name
    if glyph_name.endswith(f'.{script_code}'):
        glyph_names.append(glyph_name)

# swap Latin and Indic specific punctuation
for glyph_name in glyph_names:
    # gather information
    base_name = glyph_name.split('.')[0]
    indic = font[glyph_name]
    latin = font[base_name]

    # swap
    latin.name = f'{base_name}.latn'
    indic.name = base_name
    indic.unicode = latin.unicode
    latin.unicode = None

# Save UFO
font.changed()
font.save()
font.close()
