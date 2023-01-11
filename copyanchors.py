#!/usr/bin/python3

from ufoLib2.objects import Font
from fontParts.world import *
import json
import math
import argparse

# Open UFO
parser = argparse.ArgumentParser(description='Copy anchors from one UFO to another, correcting for the italic angle')
parser.add_argument('-i', '--italic', help='Fonts come from legacy (italic) fonts', action='store_true')
parser.add_argument('-l', '--latin', help='JSON file of Latin specific anchors to ignore')
parser.add_argument('source', help='Source UFO')
parser.add_argument('dest', help='Destination UFO')
args = parser.parse_args()

print(f'Copy anchors from {args.source} to {args.dest}')

dest_font = Font.open(args.dest)
italic_angle_degrees = dest_font.info.italicAngle
if not italic_angle_degrees:
    italic_angle_degrees = 0
italic_angle = math.radians(italic_angle_degrees)
dest_font.close()

source_font = OpenFont(args.source)
dest_font = OpenFont(args.dest)

# metrics from the font
upm = source_font.info.unitsPerEm
beltline = upm / 2

# latin specific anchors
latin_anchors = list()
if args.latin:
    with open(args.latin) as latin_anchor_file:
        latin_anchor_data = json.load(latin_anchor_file)
        latin_anchors = latin_anchor_data['base'] + latin_anchor_data['mark']

for source_glyph in source_font:

    anchors = dict()

    is_mark = False
    for source_anchor in source_glyph.anchors:
        # only process anchors for the non-latin script
        if source_anchor.name in latin_anchors:
            continue
        # determine if the glyph is a mark
        if source_anchor.name.startswith('_'):
            is_mark = True
        # record all anchor information in the source font
        anchor = anchors[source_anchor.name] = dict()
        anchor['x'] = source_anchor.x
        anchor['y'] = source_anchor.y

    # remove all the non-latin anchors in the destination font,
    # but first store the x location if needed
    try:
        dest_glyph = dest_font[source_glyph.name]
    except KeyError:
        continue
    for dest_anchor in dest_glyph.anchors:
        if dest_anchor.name in latin_anchors:
            continue
        if args.italic and is_mark:
            anchors[dest_anchor.name]['x'] = dest_anchor.x
        dest_glyph.removeAnchor(dest_anchor)

    # determine if the glyph is empty, a base glyph, above mark, or below mark
    baseline = 0
    bounds = source_glyph.bounds
    if bounds is not None:
        (xmin, ymin, xmax, ymax) = bounds
        if is_mark:
            if ymax < beltline:
                # below mark
                baseline = ymax
            else:
                # above mark
                baseline = ymin

    # add anchors to destination based on the source
    for anchor_name in anchors:
        anchor = anchors[anchor_name]

        # height (could be negative) above baseline
        height = anchor['y'] - baseline

        # amount to move anchor right (could be negative)
        italic_offset = int(-math.tan(italic_angle) * height)

        # add anchor to destination font
        dest_glyph.appendAnchor(anchor_name, (anchor['x'] + italic_offset, anchor['y']))

dest_font.changed()
dest_font.save()
dest_font.close()
