#!/usr/bin/python3

from fontParts.world import *
import fontTools.unicodedata
import csv
import sys
from operator import attrgetter
import argparse


class GlyphData(object):

    def __init__(self, name, new_name, usv, languages, features, sort_unicode, sort_script, sort_tail = ''):
        self.name = name
        self.new_name = new_name
        self.usv = usv
        self.languages = languages
        self.features = features
        self.sort_unicode = sort_unicode
        self.sort_script = sort_script
        self.sort_tail = sort_tail
        self.design = -1


def format_codepoint(codepoint):
    """Format a codepoint (integer) to a USV (at least 4 hex digits)"""
    usv = ''
    if codepoint:
        usv = f'{codepoint:04X}'
    return usv


def is_bmp(codepoint):
    """Determine if a codepoint (interger) is in the BMP"""
    return codepoint <= 0xffff


def make_row(glyph_name, ps_name, sort_final, sort_design, usv, tag, feat, args):
    """Return arguments, omitting ps_name if no renaming needs to be done"""
    row = [glyph_name, sort_final, sort_design, usv]
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
parser.add_argument('-g', '--glyphsapp', help='GlyphsApp script extension to strip from glyph names')
parser.add_argument('-v', '--virama', help='Codepoint (hex) of virama to use when the inherent vowel was killed')
parser.add_argument('-l', '--langs', help='File containing which languages affect which glyphs')
parser.add_argument('-f', '--feats', help='File containing which features affect which glyphs')
parser.add_argument('-s', '--script', help='Primary script of font to sort glyphs at the end of the font')
parser.add_argument('aglfn', help='Adobe Glyph List For New Fonts')
parser.add_argument('ufo', help='UFO to read')
parser.add_argument('csv', help='CSV file to output', nargs='?', default='glyph_data.csv')
parser.add_argument('--version', action='version', version='%(prog)s 0.4')
args = parser.parse_args()

script_id = ''
if args.glyphsapp:
    script_id = '-' + args.glyphsapp

# Load information for tuning a font (based on language or features)
languages = tune_information(args.langs)
features = tune_information(args.feats)

# Load Adobe Glyph List For New Fonts (AGLFN)
aglfn = dict()
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
        aglfn[int(usv, 16)] = aglfn_name

# Open UFO
font = OpenFont(args.ufo)

# Gather data from the UFO
cmap = dict()
for glyph in font:
    if glyph.unicode:
        glyph_name = glyph.name
        cmap[glyph_name] = glyph.unicode

skip_export = font.lib.get('public.skipExportGlyphs', [])

# Create glyph data CSV file
headers = ('glyph_name', 'ps_name', 'sort_final', 'sort_design', 'USV', 'bcp47tags', 'Feat')
otspec = ('.notdef', '.null', 'nonmarkingreturn')

glyphs = list()
new_names = set()
for glyph in font:
    # Handle the first three specially named glyphs
    if glyph.name in otspec:
        gd = GlyphData(glyph.name, glyph.name, '', '', '', -1, 0)
        glyphs.append(gd)
        continue

    # Ignore glyphs that are marked for not exporting into the final TTF
    if glyph.name in skip_export:
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
    if script_id and base_ligature_name.endswith(script_id):
        latin_script = False
        base_ligature_name = base_ligature_name.replace(script_id, '')
    for base_name in base_ligature_name.split('_'):
        # Glyphs used only for building component glyphs generally start with _
        # and will not have a codepoint and do not need to be processed here.
        if base_name == '':
            break

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

    if len(codepoints) > 0:
        if codepoints[0] in aglfn:
            # If a character is in the AGLFN or based on it use the AGLFN base name
            new_name = aglfn[codepoints[0]]
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
            new_name = ligature_prefix + new_ligature_name

        new_name += dot_name + suffix_name

    usv = ''
    sort_tail = ''
    if suffix_name == '':
        usvs = [format_codepoint(codepoint) for codepoint in codepoints]
        usv = '_'.join(usvs)
    else:
        sort_tail = suffix_name

    # Some glyphs are not associated with a codepoint so sort them
    # at the end, in alphabetical order.
    # This is the default if none of the conditions below matches.
    sort_unicode = sys.maxunicode

    # Sort by the codepoint associated with the first part of a ligature,
    # or the codepoint of the base name of the glyph if not a ligature
    # (ie, sort glyph a.alt next to glyph a, even though a.alt is not encoded).
    if len(codepoints) > 0:
        sort_unicode = codepoints[0]

    # For design, sort by the last codepoint (converted to a string) in a ligature 
    if len(codepoints) > 1:
        sort_tail = format_codepoint(codepoints[-1])

    # Sort by the codepoint of the character if not a ligature,
    # even if the name looks like it should be a ligature,
    # due to having an underscore in the glyph name.
    if glyph.unicode:
        sort_unicode = glyph.unicode

    # Retrieve optional language and features information
    glyph_languages = languages.get(glyph.name, '')
    glyph_features = features.get(glyph.name, '')

    # Group characters from main script at the end
    sort_script = 0
    if args.script in fontTools.unicodedata.script_extension(sort_unicode):
        sort_script = 1

    # Record glyph data for later sorting
    gd = GlyphData(glyph.name, new_name, usv, glyph_languages, glyph_features, sort_unicode, sort_script, sort_tail)
    glyphs.append(gd)

    # Check to see if new names are unique
    if not args.uni:
        if new_name in new_names:
            print(f'New name {new_name} in glyph {glyph.name} is already used')
        new_names.add(new_name)


# Output data
with open(args.csv, 'w', newline='') as glyph_data_file:
    glyph_data = csv.writer(glyph_data_file, lineterminator='\n')
    row = make_row(headers[0], headers[1], headers[2], headers[3], headers[4], headers[5], headers[6], args)
    glyph_data.writerow(row)

    glyphs.sort(key=attrgetter('sort_script', 'sort_tail', 'sort_unicode', 'new_name', 'name'))
    sort_count = 0
    for gd in glyphs:
        gd.design = sort_count
        sort_count += 1

    glyphs.sort(key=attrgetter('sort_script', 'sort_unicode', 'new_name', 'name'))
    sort_count = 0
    for gd in glyphs:
        row = make_row(gd.name, gd.new_name, sort_count, gd.design, gd.usv, gd.languages, gd.features, args)
        glyph_data.writerow(row)
        sort_count += 1
