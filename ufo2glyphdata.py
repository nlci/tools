#!/usr/bin/python3

from fontParts.world import *
import fontTools.unicodedata
import codecs
import csv
import sys
from operator import attrgetter
import argparse


class GlyphData(object):

    def __init__(self, name, new_name, usv, languages, features, sort_mac_roman, sort_unicode, sort_group, sort_tail = ''):
        self.name = name
        self.new_name = new_name
        self.usv = usv
        self.languages = languages
        self.features = features
        self.sort_mac_roman = sort_mac_roman
        self.sort_unicode = sort_unicode
        self.effective_sort_unicode = -1
        self.sort_group = sort_group
        self.sort_tail = sort_tail
        self.design = -1


def effective_glyph_name(glyph_name):
    """Create a temporary name to handle fullwidth CJK variants of ASCII characters"""
    return glyph_name.replace('.full', 'full')


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
parser.add_argument('-a', '--actual', help='Require the use of ActualText in PDFs for the specified script')
parser.add_argument('-d', '--debug', help='Do not rename glyphs (except for dashes and length)', action='store_true')
parser.add_argument('-u', '--uni', help='Do not rename glyphs. This assumes glyphs are already AGLFN or start with u or uni', action='store_true')
parser.add_argument('-c', '--case', help='Group case pairs together for the specified script')
parser.add_argument('-g', '--glyphsapp', help='GlyphsApp script extension to strip from glyph names')
parser.add_argument('--scriptcode', help='Short script code for output')
parser.add_argument('-v', '--virama', help='Codepoint (hex) of virama to use when the inherent vowel was killed')
parser.add_argument('-t', '--tail', help='Sort design should group glyphs that end with the same name part', action='store_true')
parser.add_argument('-l', '--langs', help='File containing which languages affect which glyphs')
parser.add_argument('-f', '--feats', help='File containing which features affect which glyphs')
parser.add_argument('-r', '--related', help='Group related characters together', action='store_true')
parser.add_argument('-m', '--macroman', help='Use the same order as MacRoman for the characters at the start of the font', action='store_true')
parser.add_argument('-s', '--sort', help='Primary script of font to sort glyphs at the end of the font')
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
        glyph_name = effective_glyph_name(glyph.name)
        cmap[glyph_name] = glyph.unicode

# skip_export = font.lib.get('public.skipExportGlyphs', [])

# MacRoman codepage
modify_mac_roman = {
    0x03A9: 0x2126,  # GREEK CAPITAL LETTER OMEGA -> OHM SIGN
    0x20AC: 0x00A4,  # EURO SIGN -> CURRENCY SIGN
    0xF8FF: 0x25CC,  # Apple logo -> DOTTED CIRCLE
}

mac_roman = dict()
for i in range(256):
    mac_codepoint = i.to_bytes(1, 'big')
    mac_char = codecs.decode(mac_codepoint, encoding='mac_roman')
    mac_usv = ord(mac_char)
    mac_usv = modify_mac_roman.get(mac_usv, mac_usv)
    mac_roman[mac_usv] = i

# Create glyph data CSV file
headers = ('glyph_name', 'ps_name', 'sort_final', 'sort_design', 'USV', 'bcp47tags', 'Feat')
otspec = ('.notdef', '.null', 'nonmarkingreturn')

glyphs = list()
new_names = set()
for glyph in font:
    # Handle the first three specially named glyphs
    if glyph.name in otspec:
        gd = GlyphData(glyph.name, glyph.name, '', '', '', -1, -1, -1)
        glyphs.append(gd)
        continue

    # Ignore glyphs that are marked for not exporting into the final TTF
    # if glyph.name in skip_export:
    #     continue

    # Output the data for the rest of the glyphs
    glyph_name = effective_glyph_name(glyph.name)

    # Split off the suffix (the text after after the full stop)
    # and the script ID, if either (or both) exist.
    glyph_name_parts = glyph_name.partition('.')
    ligature_name = glyph_name_parts[0]
    dot_name = glyph_name_parts[1]
    suffix_name = glyph_name_parts[2]
    addback_remaining = dot_name + suffix_name

    # Find the codepoint of each part of the ligature
    codepoints = list()
    latin_script = True
    addback_ligature_name = base_ligature_name = ligature_name
    if script_id and base_ligature_name.endswith(script_id):
        latin_script = False
        base_ligature_name = base_ligature_name.replace(script_id, '')
        if args.scriptcode:
            addback_ligature_name = base_ligature_name + args.scriptcode
    addback_name = addback_ligature_name + addback_remaining
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
            print(f'Info: {glyph.name} does not have base {base_name}')

    # Construct new glyph name
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

        new_name += addback_remaining
    else:
        new_name = addback_name

    usv = ''
    sort_tail = ''
    if suffix_name == '':
        usvs = [format_codepoint(codepoint) for codepoint in codepoints]
        usv = '_'.join(usvs)
    elif args.tail:
        sort_tail = suffix_name

    # Some glyphs are not associated with a codepoint so sort them
    # at the end, in alphabetical order.
    # This is the default if none of the conditions below matches.
    sort_unicode = sys.maxunicode
    sort_group = 2
    design_group = 2
    if args.related:
        sort_group = 1
        design_group = 1

    # Sort by the codepoint associated with the first part of a ligature,
    # or the codepoint of the base name of the glyph if not a ligature
    # (ie, sort glyph a.alt next to glyph a, even though a.alt is not encoded).
    if len(codepoints) > 0:
        sort_unicode = codepoints[0]

    # For design, if specified, sort by the last codepoint (converted to a string) in a ligature
    if args.tail and len(codepoints) > 1:
        sort_tail = format_codepoint(codepoints[-1])

    # Sort by the codepoint of the character if not a ligature,
    # even if the name looks like it should be a ligature,
    # due to having an underscore in the glyph name.
    sort_mac_roman = -1
    if glyph.unicode:
        sort_unicode = glyph.unicode
        sort_group = 1
        design_group = 1
        # Unless character is in the MacRoman codepage then the character
        # should be in the first group of characters in the font.
        if args.macroman and sort_unicode in mac_roman:
            sort_mac_roman = mac_roman[sort_unicode]
            sort_group = 0

    # Retrieve optional language and features information
    glyph_languages = languages.get(glyph.name, '')
    glyph_features = features.get(glyph.name, '')

    # Group characters from main script at the end
    if args.sort in fontTools.unicodedata.script_extension(sort_unicode):
        sort_group = 3
        design_group = 3
        if not glyph.unicode and not args.related:
            sort_group = 4
            design_group = 4

    # Do not rename glyphs (except for dashes) in the specified script
    if args.actual in fontTools.unicodedata.script_extension(sort_unicode):
        new_name = addback_name

    # Do not rename glyphs (except for dashes and glyph length) for use with a debugger
    if args.debug:
        new_name = addback_name

    # Glyph names in a TTF file cannot have dashes in them
    new_name = new_name.replace('-', '')

    # Glyph names in a TTF file should not be longer than 31 charactrers
    trim_name = new_name[:31]
    if trim_name != new_name:
        print(f'Warning: for {glyph.name} the name {new_name} was trimmed to {trim_name}')
    new_name = trim_name

    # Record glyph data for later sorting
    gd = GlyphData(glyph.name, new_name, usv, glyph_languages, glyph_features, sort_mac_roman, sort_unicode, sort_group, sort_tail)
    glyphs.append(gd)

    # Check to see if new names are unique
    if not args.uni:
        if new_name in new_names:
            print(f'Warning: New name {new_name} for glyph {glyph.name} is already used')
        new_names.add(new_name)

# Group case pairs together
if args.case:
    for gd in glyphs:
        if args.case in fontTools.unicodedata.script_extension(gd.sort_unicode):
            glyph_name = gd.name.replace(script_id, '')
            glyph_name = glyph_name.title() + script_id
            gd.sort_unicode = cmap.get(glyph_name, gd.sort_unicode)

# Output data
with open(args.csv, 'w', newline='') as glyph_data_file:
    glyph_data = csv.writer(glyph_data_file, lineterminator='\n')
    row = make_row(headers[0], headers[1], headers[2], headers[3], headers[4], headers[5], headers[6], args)
    glyph_data.writerow(row)

    glyphs.sort(key=attrgetter('sort_tail', 'sort_unicode', 'new_name', 'name'))
    sort_count = 0
    for gd in glyphs:
        gd.design = sort_count
        sort_count += 1

    glyphs.sort(key=attrgetter('sort_group', 'sort_mac_roman', 'sort_unicode', 'new_name', 'name'))
    sort_count = 0
    for gd in glyphs:
        row = make_row(gd.name, gd.new_name, sort_count, gd.design, gd.usv, gd.languages, gd.features, args)
        glyph_data.writerow(row)
        sort_count += 1
