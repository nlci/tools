#!/bin/bash

export ufo=results/ufo
export src=source
# grep -E "faces|styles" wscript | grep = > wscript.py
rm -f *.sfd

pushd ${src}/archive
prep=unhinted
tmp=tmp.ttf
rm -rf $prep
mkdir $prep
for ttf in *.ttf
do
    rm -f tmp.ttf
    hackos2 -t 0 $ttf $tmp
    ttfstriphints $tmp ${prep}/${ttf}
    rm -f $tmp
done
popd

rm -f ${src}/*-???*.sfd
export FLOWARGS=""
smith distclean -l
smith configure -l
smith build -l

pushd ${ufo}
for ttf in *.ttf
do
    echo $ttf
    sfd="$(basename $ttf .ttf).sfd"
    fontforge -script ${nlci}/ttf2sfd.ff $ttf $sfd
done
popd
