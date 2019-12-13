#!/usr/bin/python3

from fontParts.world import *
import csv
import sys

# Open UFO and glyph_data CSV
ufo = sys.argv[1]
font = OpenFont(ufo)

csv_file = open(sys.argv[2])
gd = csv.DictReader(csv_file)

# Compare glyph names in UFO and CSV file

## Read glyph names from UFO
ufo_glyph_list = set()
for glyph in font:
    ufo_glyph_list.add(glyph.name)

## Read glyph names from CSV file
gd_glyph_list = set()
for row in gd:
    gd_glyph_list.add(row['glyph_name'])

## Show differences
length = len(gd_glyph_list)
print(f'error:   missing from glyph_data.csv which has {length} glyphs')
for glyph_name in ufo_glyph_list - gd_glyph_list:
    print(f'{glyph_name}')

length = len(ufo_glyph_list)
print(f'warning: missing from UFO glyph list which has {length} glyphs')
for glyph_name in gd_glyph_list - ufo_glyph_list:
    print(f'{glyph_name}')
