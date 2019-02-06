#!/bin/bash

export PYTHONPATH=${nlci}:/usr/local/lib/python3.6/site-packages

cp -p -v ${ufo}/*.sfd ${src}

sort -o cs/charis/pre.txt cs/charis/composite.txt cs/charis/decomposition.txt
sort -o cs/gentium/pre.txt cs/gentium/composite.txt cs/gentium/decomposition.txt
sort -o cs/exo/pre.txt cs/exo/composite.txt cs/exo/decomposition.txt
python addchars.py ${src}
