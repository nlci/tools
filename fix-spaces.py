#!/usr/bin/python3

from fontParts.world import *
import sys

# Open UFO
ufo = sys.argv[1]
font = OpenFont(ufo)

# Modify UFO

# Find the needed space glyphs
for glyph in font:
    if glyph.unicode == 0x0020:
        space = glyph
    if glyph.unicode == 0x002E:
        period = glyph
    if glyph.unicode == 0x0030:
        zero = glyph
    if glyph.unicode == 0x00A0:
        nbspace = glyph
    if glyph.unicode == 0x2007:
        figurespace = glyph
    if glyph.unicode == 0x2008:
        punctuationspace = glyph
    if glyph.unicode == 0x2003:
        emspace = glyph
    if glyph.unicode == 0x2002:
        enspace = glyph
    if glyph.unicode == 0x2000:
        enquad = glyph
    if glyph.unicode == 0x2001:
        emquad = glyph
    if glyph.unicode == 0x2004:
        threeperemspace = glyph
    if glyph.unicode == 0x2005:
        fourperemspace = glyph
    if glyph.unicode == 0x2006:
        sixperemspace = glyph
    if glyph.unicode == 0x2009:
        thinspace = glyph
    if glyph.unicode == 0x200A:
        hairspace = glyph
    if glyph.unicode == 0x202F:
        nnbspace = glyph

# Set width of spaces correctly
nbspace.width = space.width
figurespace.width = zero.width
punctuationspace.width = period.width

upm = font.info.unitsPerEm
em = upm

emspace.width = upm
enspace.width = em/2
enquad.width = em/2
emquad.width = em
threeperemspace.width = em/3
fourperemspace.width = em/4
sixperemspace.width = em/6
thinspace.width = em/5
hairspace.width = em/13
nnbspace.width = thinspace.width

# Save UFO
font.changed()
font.save()
font.close()
