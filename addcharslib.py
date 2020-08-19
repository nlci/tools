#!/bin/python3

import os
import os.path
import sys

from wscript import *

# Latin (and others)
charis = '../../../latn/fonts/charis/source/CharisSIL'
gentium = '../../../latn/fonts/gentium_local/instances/GentiumBookPlus'
sourcesans = '../../../latn/fonts/source/SourceSansPro'
exo = '../../../latn/fonts/exo/sources/instance_ufos/Exo'
runic = '../../../../builds/noto-source/src/NotoSansRunic/NotoSansRunic'


def modifyFile(scale, fontname, f, sn, lsn = '', chars = 'main_import.txt'):
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
    aglfn = os.path.join(nlci, 'aglfn-nr.csv')
    fontpath = eval(fontname)
    latin = f'{fontpath}-{lsn}.ufo'

    # List of glyphs to copy
    glyphs = os.path.join(src, 'copyglyphs', f'{fontname}-{lsn}-{f}-{sn}.txt')

    cmd = f'psfgetglyphnames -a {aglfn} -i cs/{chars} {latin} {glyphs}'
    print(cmd)
    os.system(cmd)

    cmd = f'psfcopyglyphs --rename rename --unicode usv --scale {scale} -i {glyphs} -s {latin} {ufo}'
    print(cmd)
    os.system(cmd)
