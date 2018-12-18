#!/bin/python

import os
import os.path
import sys

from wscript import *

charis = '../../../latn/fonts/charis_local/5.000/zip/unhinted/CharisSIL'
gentium = '../../../latn/fonts/gentium_local/basic/1.102/zip/unhinted/GenBkBas'
annapurna = '../../../deva/fonts/annapurna_local/1.203/zip/unhinted/AnnapurnaSIL-'
panini = '../../../deva/fonts/panini-master/source/Panini'
exo = '../../../latn/fonts/exo/1.500/zip/unhinted/1000/Exo-'
deva = '../../../deva/fonts/panini/source/'
thiruvalluvar = '../../../taml/fonts/thiruvalluvar/source/ThiruValluvar'
vaigai = '../../../taml/fonts/thiruvalluvar/source/Vaigai'
exo = '../../../latn/fonts/exo/1.500/zip/unhinted/1000/Exo-'

def runCommand(cmd, ifont, ofont):
    cmd = 'ffcopyglyphs' + ' -f ' + cmd + ' ' + ifont + ' ' + ofont
    print cmd
    os.system(cmd)

def findFile(filename):
    return os.path.join(sys.argv[1], filename)

def modifyFile(cmd, filename):
    tmp = 'tmp.sfd'
    os.rename(findFile(filename), tmp)
    runCommand(cmd, tmp, findFile(filename))
    os.remove(tmp)
