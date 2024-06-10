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

for punct in ('figuredash', 'endash', 'emdash', 'horizontalbar', 'quoteleft', 'quoteright', 'quotedblleft', 'quotedblright'): # 'minus'
    indic = font[punct]
    latin = font[f'{punct}.latn']

    # dashes
    if font.info.familyName != 'Gir':
        if punct == 'figuredash':
            indic.width = zero.width
        if punct == 'endash':
            indic.scaleBy((nscale, 0.78), width=True, height=False)
        if punct == 'emdash':
            indic.scaleBy((mscale, 0.78), width=True, height=False)
        if punct == 'horizontalbar':
            indic.scaleBy((hscale, 0.78), width=True, height=False)

    # quotes
    if punct.startswith('quote'):
        if punct.endswith('left'):
            indic.leftMargin = latin.leftMargin
        if punct.endswith('right'):    
            indic.rightMargin = latin.rightMargin

# Save UFO
font.changed()
font.save()
font.close()
