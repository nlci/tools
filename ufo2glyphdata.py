#!/usr/bin/python3

from fontParts.world import *
import csv
import sys
from operator import attrgetter
import argparse


class GlyphData(object):

    def __init__(self, name, new_name, usv, languages, features, sort_unicode):
        self.name = name
        self.new_name = new_name
        self.usv = usv
        self.languages = languages
        self.features = features
        self.sort_unicode = sort_unicode


def format_codepoint(codepoint):
    """Format a codepoint (integer) to a USV (at least 4 hex digits)"""
    usv = ''
    if codepoint:
        usv = f'{codepoint:04X}'
    return usv


def is_bmp(codepoint):
    """Determine if a codepoint (interger) is in the BMP"""
    return codepoint <= 0xffff


def make_row(glyph_name, ps_name, sort_final, usv, tag, feat, args):
    """Return arguments, omitting ps_name if no renaming needs to be done"""
    row = [glyph_name, sort_final, usv]
    if not args.uni:
        row.insert(1, ps_name)
    if args.langs:
        row.append(tag)
    if args.feats:
        row.append(feat)
    return row


def tune_information(filename):
    """Read information for tuning a font (language or features)"""
    tunes = dict()
    if filename:
        with open(filename, 'r', newline='') as tune_file:
            reader = csv.reader(tune_file)
            for line in reader:
                glyph_name = line[0]
                tune = line[1].replace(' ', ',')
                tunes[glyph_name] = tune
    return tunes


# Command line arguments
parser = argparse.ArgumentParser(description='Generate glyph_data.csv from UFO')
parser.add_argument('-u', '--uni', help='Do not rename glyphs. This assumes glyphs are already AGLFN or start with u or uni', action='store_true')
parser.add_argument('-s', '--script', help='GlyphsApp script extension to strip from glyph names')
parser.add_argument('-v', '--virama', help='Codepoint (hex) of virama to use when the inherent vowel was killed')
parser.add_argument('-l', '--langs', help='File containing which languages affect which glyphs')
parser.add_argument('-f', '--feats', help='File containing which features affect which glyphs')
parser.add_argument('aglfn', help='Adobe Glyph List For New Fonts')
parser.add_argument('ufo', help='UFO to read')
parser.add_argument('csv', help='CSV file to output', nargs='?', default='glyph_data.csv')
parser.add_argument('--version', action='version', version='%(prog)s 0.3')
args = parser.parse_args()

script_id = ''
if args.script:
    script_id = '-' + args.script

# Load information for tuning a font (based on language or features)
languages = tune_information(args.langs)
features = tune_information(args.feats)

# Load Adobe Glyph List For New Fonts (AGLFN)
aglfn = list()
with open(args.aglfn, newline='') as aglfn_file:
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
font = OpenFont(args.ufo)

# Gather data from the UFO
cmap = dict()
for glyph in font:
    if glyph.unicode:
        glyph_name = glyph.name
        cmap[glyph_name] = glyph.unicode

# Create glyph data CSV file
headers = ('glyph_name', 'ps_name', 'sort_final', 'USV', 'bcp47tags', 'Feat')
otspec = ('.notdef', '.null', 'nonmarkingreturn')

most_glyphs = list()
new_names = set()
for glyph in font:
    # Don't output again the first three specially named glyphs
    if glyph.name in otspec:
        continue

    # Output the data for the rest of the glyphs
    glyph_name = glyph.name
    new_name = glyph_name

    # Split off the suffix (the text after after the full stop)
    # and the script ID, if either (or both) exist.
    glyph_name_parts = glyph_name.partition('.')
    ligature_name = glyph_name_parts[0]
    dot_name = glyph_name_parts[1]
    suffix_name = glyph_name_parts[2]

    # Find the codepoint of each part of the ligature
    codepoints = list()
    latin_script = True
    base_ligature_name = ligature_name
    if args.script and base_ligature_name.endswith(script_id):
        latin_script = False
        base_ligature_name = base_ligature_name.replace(script_id, '')
    for base_name in base_ligature_name.split('_'):
        found = False
        if args.virama:
            # Look for the name with the inherent vowel appended
            base_name_plus = base_name + 'a' + script_id
            if base_name_plus in cmap:
                codepoint = cmap[base_name_plus]
                codepoints.append(codepoint)
                # Also include the virama since that is what caused
                # the inherent vowel to be removed from the glyph name
                codepoints.append(int(args.virama, 16))
                found = True
        if not found:
            base_name_plus = base_name
            if not latin_script:
                base_name_plus = base_name + script_id
            if base_name_plus in cmap:
                codepoint = cmap[base_name_plus]
                codepoints.append(codepoint)
                found = True
        if not found:
            print(f'Cannot find base {base_name} in font for glyph {glyph.name}')

    if ligature_name in aglfn:
        # Keep glyph names listed in or based on the AGLFN unchanged
        pass
    elif len(codepoints) == 0:
        # Some glyphs are not associated with a codepoint so we sort them at the end
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
        new_ligature_name_parts = [glyph_prefix + format_codepoint(codepoint) for codepoint in codepoints]
        new_ligature_name = sep.join(new_ligature_name_parts)
        new_name = ligature_prefix + new_ligature_name + dot_name + suffix_name

    usv = ''
    if suffix_name == '':
        usvs = [format_codepoint(codepoint) for codepoint in codepoints]
        usv = ' '.join(usvs)
    # usv = format_codepoint(glyph.unicode)

    # Sorting is determined based on the codepoint
    # associated with the first part of a ligature,
    # or the codepoint of the character if not a ligature,
    # or by alphabetical order if there is no codepoint
    # associated with the glyph.
    sort_unicode = sys.maxunicode
    if len(codepoints) > 0:
        sort_unicode = codepoints[0]
    if glyph.unicode:
        sort_unicode = glyph.unicode

    # Retrieve optional language and features information
    glyph_languages = languages.get(glyph.name, '')
    glyph_features = features.get(glyph.name, '')

    # Record glyph data for later sorting.
    gd = GlyphData(glyph.name, new_name, usv, glyph_languages, glyph_features, sort_unicode)
    most_glyphs.append(gd)

    # Check to see if new names are unique
    if not args.uni:
        if new_name in new_names:
            print(f'New name {new_name} in glyph {glyph.name} is already used')
        new_names.add(new_name)


# Output data
with open(args.csv, 'w', newline='') as glyph_data_file:
    glyph_data = csv.writer(glyph_data_file, lineterminator='\n')
    row = make_row(headers[0], headers[1], headers[2], headers[3], headers[4], headers[5], args)
    glyph_data.writerow(row)
    sort_count = 0

    for first_glyphs in otspec:
        row = make_row(first_glyphs, first_glyphs, sort_count, '', '', '',  args)
        glyph_data.writerow(row)
        sort_count += 1

    most_glyphs.sort(key=attrgetter('sort_unicode', 'new_name', 'name'))
    for gd in most_glyphs:
        row = make_row(gd.name, gd.new_name, sort_count, gd.usv, gd.languages, gd.features, args)
        glyph_data.writerow(row)
        sort_count += 1
