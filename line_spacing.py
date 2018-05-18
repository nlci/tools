#!/usr/bin/python3

from fontParts.world import *
import sys

# Open UFO
ufo = sys.argv[1]
font = OpenFont(ufo)

# Line spacing metrics
metrics = {
    # taml
    'ThiruValluvar': (-1012, 2152), # v0.271 had (-1029, 2650)
    'Auvaiyar': (-494, 1042),
    'Vaigai': (-494, 1057)
    }

metric = metrics[font.info.familyName]
descender, ascender = metric

# Modify UFO
font.info.openTypeOS2WinAscent = ascender
font.info.openTypeOS2WinDescent = -descender

font.info.openTypeOS2TypoAscender = ascender
font.info.openTypeOS2TypoDescender = descender
font.info.openTypeOS2TypoLineGap = 0

font.info.openTypeHheaAscender = ascender
font.info.openTypeHheaDescender = descender
font.info.openTypeHheaLineGap = 0

# Save UFO
font.changed()
font.save()
font.close()
