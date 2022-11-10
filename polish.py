#!/usr/bin/python3

from fontParts.world import *
import sys

# Open UFO
ufo = sys.argv[1]
font = OpenFont(ufo)

# Modify UFO
def ratio(source, dash):
    hyphen = font[source]
    target = font[dash]
    return target.width/hyphen.width

zero = font['zero']
nscale = ratio('hyphen.latn', 'endash.latn')
mscale = ratio('hyphen.latn', 'emdash.latn')
hscale = (nscale + mscale) / 2

for dash in ('figuredash', 'endash', 'emdash', 'horizontalbar', 'minus'):
    indic = font[dash]
    latin = font[f'{dash}.latn']
    if dash == 'figuredash' or 'minus':
        indic.width = zero.width
    if font.info.familyName != 'Auvaiyar':
        if dash == 'endash':
            indic.scaleBy((nscale, 0.78), width=True, height=False)
        if dash == 'emdash':
            indic.scaleBy((mscale, 0.78), width=True, height=False)
        if dash == 'horizontalbar':
            indic.scaleBy((hscale, 0.78), width=True, height=False)
    # indic.leftMargin = latin.leftMargin
    # indic.rightMargin = latin.rightMargin

# Save UFO
font.changed()
font.save()
font.close()
