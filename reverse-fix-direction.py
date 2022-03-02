#!/usr/bin/python3

from fontParts.world import *
import sys

# Open UFO
ufo = sys.argv[1]
font = OpenFont(ufo)

mode = sys.argv[2]

# Modify UFO

all_fixes = {
    # deva
    'Kautilya': ['abbreviationsign'],
    'Maurya': ['comma.deva', 'period.deva', 'candrabindu', 'na.half', 'ra.sub', 'nukta', 'nukta_umatra', 'nukta_uumatra', 'umatra.rphf', 'uumatra.low', 'uumatra.rphf', 'virama', 'fa.half', 'dottedcircle'],

    # knda
    'Badami': ['uvowel', 'sevenknda'],
    'Kaveri': ['fa.sub'],

    # taml
    'Auvaiyar': ['nga_iimatra', 'lla_umatra', 'ma_umatra'],
    }
fixes = all_fixes.get(font.info.familyName, [])

if mode == 'init':
    # Contour direction
    for glyph in font:
        # print(glyph.name)
        # Remove stray contours
        for contour in glyph.contours:
            if len(contour) <= 2:
                glyph.removeContour(contour)

        # Reverse contour direction since the glyphs came from
        # a TTF font and the source should have PostScript curves
        for contour in glyph.contours:
            contour.reverse()

        # Some glyphs had incorrect curve direction to start with
        if glyph.name in fixes:
            glyph.correctDirection()

elif mode == 'import':
    glyph = font['llvocalicmatra']
    glyph.correctDirection()

# Save UFO
font.changed()
font.save()
font.close()
