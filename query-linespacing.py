#!/usr/bin/python3

from fontParts.world import *
import tabulate
import argparse

# Command line arguments
parser = argparse.ArgumentParser(description='Show line spacing information in a UFO')
parser.add_argument('ufo', help='UFO to read')
parser.add_argument('--version', action='version', version='%(prog)s 0.1')
args = parser.parse_args()

# Open UFO
font = OpenFont(args.ufo)

# Query UFO
rows = list()

rows.append(['ascender', font.info.ascender])
rows.append(['OS2WinAscent', font.info.openTypeOS2WinAscent])
rows.append(['OS2TypoAscender', font.info.openTypeOS2TypoAscender])
rows.append(['HheaAscender', font.info.openTypeHheaAscender])

rows.append(['descender', font.info.descender])
rows.append(['OS2WinDescent', font.info.openTypeOS2WinDescent])
rows.append(['OS2TypoDescender', font.info.openTypeOS2TypoDescender])
rows.append(['HheaDescender', font.info.openTypeHheaDescender])

rows.append(['OS2TypoLineGap', font.info.openTypeOS2TypoLineGap])
rows.append(['HheaLineGap', font.info.openTypeHheaLineGap])

output = tabulate.tabulate(rows, tablefmt='plain')
print(output)

# Save UFO
# font.changed()
# font.save()
# font.close()
