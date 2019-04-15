#!/bin/python3

import os
import os.path
import sys

from wscript import *

# Latin
charis = '../../../latn/fonts/charis/source/CharisSIL'
gentium = '../../../latn/fonts/gentium_local/instances/GentiumBookPlus'
sourcesans = '../../../latn/fonts/source/SourceSansPro'
exo = '../../../latn/fonts/exo/sources/instances/Exo'

def modifyFile(scale, fontname, f, sn, lsn = ''):
    # File locations
    src = sys.argv[1]
    nlci = sys.argv[2]

    # UFO to modify
    sn = sn.replace(' ', '')
    ufo = f + '-' + sn + '.ufo'
    ufo = os.path.join(src, ufo)

    # Unique Latin style
    if lsn == '':
        lsn = sn

    # Input data
    aglfn = os.path.join(nlci, 'aglfn-nr.txt')
    fontpath = eval(fontname)
    latin = f'{fontpath}-{lsn}.ufo'

    # List of glyphs to copy
    glyphs = os.path.join(src, f'copyglyphs-{fontname}-{lsn}-{f}-{sn}.txt')

    cmd = f'psfgetglyphnames -a {aglfn} -i cs/main_import.txt {latin} {glyphs}'
    print(cmd)
    os.system(cmd)

    cmd = f'psfcopyglyphs --rename rename --unicode usv --scale {scale} -i {glyphs} -s {latin} {ufo}'
    print(cmd)
    os.system(cmd)
