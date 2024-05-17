#!/bin/python3

import os
import os.path
import sys

from wscript import *

# Latin (and others)
charis = '../../../latn/fonts/charis/source/masters/CharisSIL'
gentium = '../../../latn/fonts/gentium_local/instances/Gentium'
andika = '../../../latn/fonts/andika/source/Andika'
sourcesans = '../../../latn/fonts/source/SourceSansPro'
exo = '../../../latn/fonts/exo/sources/instance_ufos/Exo'
runic = '../../../../builds/noto-source/src/NotoSansRunic/NotoSansRunic'


def modifyFile(scale, fontname, f, sn, styles={}, chars='all_import.txt'):
    # File locations
    src = sys.argv[1]
    nlci = sys.argv[2]
    cs = sys.argv[3]

    # Latin style to use
    lsn = styles.get(sn, sn)
    lsn = lsn.replace(' ', '')

    # UFO to modify
    sn = sn.replace(' ', '')
    ufo = f + '-' + sn + '.ufo'
    ufo = os.path.join(src, ufo)

    # Input data
    aglfn = os.path.join(nlci, 'glyph_names.csv')
    fontpath = eval(fontname)
    latin = f'{fontpath}-{lsn}.ufo'

    # List of glyphs to copy
    glyphs = os.path.join(src, 'copyglyphs', f'{fontname}-{lsn}-{f}-{sn}.txt')

    cmd = f'psfgetglyphnames -a {aglfn} -i {cs}/{chars} {latin} {glyphs}'
    print(cmd)
    os.system(cmd)

    cmd = f'psfcopyglyphs --rename rename --unicode usv --scale {scale} -i {glyphs} -s {latin} {ufo}'
    print(cmd)
    os.system(cmd)
