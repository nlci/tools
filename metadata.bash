#!/bin/bash

export beng="../../../../beng/fonts/bhagirati/source"
export deva="../../../../deva/fonts/panini/source"
export taml="../../../../taml/fonts/thiruvalluvar/source"

pushd ${src}
rm -rf *.ufo
for sfd in *-???*.sfd
do
    echo $sfd
    fontfilename="$(basename $sfd .sfd)"
    fontforge -script ${nlci}/sfd2ufo.ff $sfd ${fontfilename}.ufo3
    mv -v ${fontfilename}.ufo3 ${fontfilename}.ufo
done
popd

pushd ${src}
for fi in ${!faces[@]} # loop over indices
do
    f=${faces[$fi]} # fi is the index into the array faces

    for si in ${!styles[@]} # loop over indices
    do
        s=${styles[$si]} # si is the index into the array styles

        ufo=${f/ /}-${s/ /}.ufo # remove spaces in both face and style strings

        echo "setting metrics in UFO ${ufo}"
        psfnormalize -p backup=0 -v 3 -p checkfix=none $ufo
        ../tools/encoding.py $ufo
        ${nlci}/heights.py $ufo
        ${nlci}/line_spacing.py $ufo

        echo "setting family ${f} and style ${s} in UFO ${ufo}"
        psfsetkeys -p backup=0 -k familyName                         -v "${f}" $ufo
        psfsetkeys -p backup=0 -k openTypeNamePreferredFamilyName    -v "${f}" $ufo
        psfsetkeys -p backup=0 -k styleName                          -v "${s}" $ufo
        psfsetkeys -p backup=0 -k openTypeNamePreferredSubfamilyName -v "${s}" $ufo
        psfsetkeys -p backup=0 -k postscriptFullName                 -v "${f} ${s}" $ufo
        psfsetkeys -p backup=0 -k styleMapFamilyName                 -v "${f} ${s}" $ufo
        psfsetkeys -p backup=0 -k styleMapStyleName                  -v "${s,,}" $ufo

        echo "setting general keys in UFO ${ufo}"
        psfsetkeys -p backup=0 -i ${nlci}/fontinfo.csv -k "openTypeNameDescription" -v "$desc_long" $ufo
        psfsetkeys -p backup=0 -i ${nlci}/lib.csv --plist lib $ufo

        echo "setting glyphsapp keys in UFO ${ufo}"
        if [ "$s" = "Bold" -o "$s" = "Bold Italic" ]
        then
            psfsetkeys -p backup=0 -k "com.schriftgestaltung.weight" -v "Bold" --plist lib $ufo
            psfsetkeys -p backup=0 -k "com.schriftgestaltung.weightValue" -v "700" --plist lib $ufo
        else
            psfsetkeys -p backup=0 -k "com.schriftgestaltung.weightValue" -v "400" --plist lib $ufo
        fi

        echo "importing glyphs in UFO ${ufo}"
        ../tools/import.bash "${f}" "${s/ /}" $ufo
        # echo "fixing glyphs in UFO ${ufo}"
        # ../tools/cleanup.py $ufo
        if [ -f composites.txt ]
        then
            echo "building composites in UFO ${ufo}"
            psfbuildcomp -i composites.txt $ufo
        fi
        echo "listing glyphs in UFO ${ufo}"
        ${nlci}/ufo2glyphdata.py $HOME/pub/doc/Adobe/agl-aglfn/aglfn.txt $ufo glyph_data-${f}.csv
    done
done

rm -rf backups
popd

echo "now running preflight"
./preflight
echo "done running preflight"
