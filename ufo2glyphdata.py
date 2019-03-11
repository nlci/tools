#!/usr/bin/python3

from fontParts.world import *
import sys
import csv
from operator import attrgetter


class GlyphData(object):

    def __init__(self, name, new_name, usv, sort_unicode):
        self.name = name
        self.new_name = new_name
        self.usv = usv
        self.sort_unicode = sort_unicode


def format_codepoint(codepoint):
    """Format a codepoint (integer) to a USV (at least 4 hex digits)"""
    usv = ''
    if codepoint:
        usv = f'{codepoint:04X}'
    return usv


def is_bmp(codepoint):
    """Determine if a codepoint (interger) is in the BMP"""

    if codepoint > 0xffff:
        return False
    return True


# Load Adobe Glyph List For New Fonts (AGLFN)
aglfn = list()
with open(sys.argv[1], newline='') as aglfn_file:
    for line in aglfn_file:

        # Ignore comments
        line = line.partition('#')[0]
        line = line.strip()

        # Ignore blank lines
        if line == '':
            continue

        # Load data
        (usv, aglfn_name, unicode_name) = line.split(';')
        aglfn.append(aglfn_name)

# Open UFO
ufo = sys.argv[2]
font = OpenFont(ufo)

# Gather data from the UFO
cmap = dict()
for glyph in font:
    if glyph.unicode:
        cmap[glyph.name] = glyph.unicode

# Create glyph data CSV file
headers = ('glyph_name', 'ps_name', 'sort_final', 'USV')
otspec = ('.notdef', '.null', 'nonmarkingreturn')

most_glyphs = list()
for glyph in font:
    # Don't output again the first three specially named glyphs
    if glyph.name in otspec:
        continue

    # Output the data for the rest of the glyphs
    new_name = glyph.name
    first_codepoint = glyph.unicode
    usv = format_codepoint(glyph.unicode)

    # Split off the modifier part (the text after after the full stop)
    glyph_name_parts = glyph.name.partition('.')
    ligature_name = glyph_name_parts[0]
    dot_name = glyph_name_parts[1]
    modify_name = glyph_name_parts[2]

    # Find the codepoint of each part of the ligature
    codepoints = list()
    for base_name in ligature_name.split('_'):
        if base_name in cmap:
            codepoint = cmap[base_name]
            codepoints.append(codepoint)
        else:
            print(f'Cannot find {base_name} in font')

    if ligature_name in aglfn:
        # Keep glyph names listed or based on the the AGLFN unchanged
        pass
    else:
        # Determine the needed format of glyph names.
        max_codepoint = max(codepoints)
        if is_bmp(max_codepoint):
            ligature_prefix = 'uni'
            glyph_prefix = ''
            sep = ''
        else:
            ligature_prefix = ''
            glyph_prefix = 'u'
            sep = '_'

        # Rename glyphs by creating a new glyph name
        new_name = ligature_prefix \
                   + sep.join([glyph_prefix + format_codepoint(codepoint) for codepoint in codepoints]) \
                   + dot_name + modify_name

    # Sorting is determined based on the codepoint associated with the first part of a ligature.
    first_codepoint = codepoints[0]

    # Record glyph data for later sorting.
    gd = GlyphData(glyph.name, new_name, usv, first_codepoint)
    most_glyphs.append(gd)


# Output data
with open(sys.argv[3], 'w', newline='') as glyph_data_file:
    glyph_data = csv.writer(glyph_data_file)
    glyph_data.writerow(headers)
    sort_count = 0

    for first_glyphs in otspec:
        row = (first_glyphs, first_glyphs, sort_count, '')
        glyph_data.writerow(row)
        sort_count += 1

    most_glyphs.sort(key=attrgetter('sort_unicode', 'new_name'))
    for gd in most_glyphs:
        row = (gd.name, gd.new_name, sort_count, gd.usv)
        glyph_data.writerow(row)
        sort_count += 1
