#!/bin/bash

export orya="../../../../orya/fonts/asika/source"
export deva="../../../../deva/fonts/panini/source"
export taml="../../../../taml/fonts/thiruvalluvar/source"

# Convert to friendly working glyph names
pushd ${src}
for sfd in *-???*.sfd
do
    echo $sfd
    perl $HOME/script/zind/bin/codepoint2name.pl -c $sfd -n tmp.sfd -m $HOME/script/zind/fonts/indictable.tsv
    mv tmp.sfd $sfd
done
popd

# Convert SFD to UFO
pushd ${src}
rm -rf *.ufo
for sfd in *-???*.sfd
do
    echo $sfd
    fontfilename="$(basename $sfd .sfd)"
    fontforge -script ${nlci}/sfd2ufo.ff $sfd ${fontfilename}.ufo3
    mv -v ${fontfilename}.ufo3 ${fontfilename}.ufo

    # Set WOFF metadata in UFOs
    # Also works around https://github.com/fontforge/fontforge/issues/4951
    fontinfo=${fontfilename}.ufo/fontinfo.plist
    head -n -3 ${fontinfo} > tmp.plist
    mv tmp.plist ${fontinfo}
    cat ${nlci}/fontinfo1.plist >> ${fontinfo}
    echo -n "<string>" >> ${fontinfo}
    echo -n $(grep "Pan " ../FONTLOG.txt) >> ${fontinfo}
    echo "</string>" >> ${fontinfo}
    cat ${nlci}/fontinfo2.plist >> ${fontinfo}
done
popd

# Initial modifications to the UFOs
for ufo in ${src}/*.ufo
do
    echo "setting metrics in UFO ${ufo}"
    psfnormalize -p backup=0 -v 3 -p checkfix=none $ufo
    ${nlci}/reverse-fix-direction.py $ufo init
    ./tools/encoding.py $ufo
    ${nlci}/heights.py $ufo
    ${nlci}/line_spacing.py $ufo

    if [ -f ${src}/delete_latin_glyphs.txt ]
    then
        echo "deleting latin glyphs (to be re-added later) in UFO ${ufo}"
        psfdeleteglyphs -i ${src}/delete_latin_glyphs.txt $ufo
    fi

    # Save needed anchors
    $HOME/script/tools/anchor-keep.py mark $nlci/anchors.json $ufo

    echo "Use script specific dashes"
    psfbuildcompgc -i ${src}/composites.glyphConstruction $ufo
done

# Add many Latin glyphs to the UFOs
pushd cs
cat main_import.txt cp1252_nf?.txt > all_import.txt
cat main_import.txt cp1252_nfc.txt > nfc_import.txt
cat main_import.txt cp1252_nfd.txt > nfd_import.txt
popd
rm -rf ${src}/copyglyphs
mkdir ${src}/copyglyphs
export PYTHONPATH=${nlci}
./addchars.py ${src} ${nlci}

# Further modifications to the UFOs using face and style names
pushd ${src}
for fi in ${!faces[@]} # loop over indices
do
    f=${faces[$fi]} # fi is the index into the array faces

    for si in ${!styles[@]} # loop over indices
    do
        s=${styles[$si]} # si is the index into the array styles

        ufo=${f/ /}-${s/ /}.ufo # remove spaces in both face and style strings

        # Restore needed anchors
        $HOME/script/tools/anchor-keep.py only $nlci/anchors.json $ufo

        # Swap Latin and Indic specific punctuation (and digits)
        ${nlci}/indic_punct.py $ufo

        # fix issues found by Font Bakery
        ${nlci}/fix-spaces.py $ufo
        ${nlci}/fix-gdef.py $ufo

        # Remove color from glyphs,
        # generally only glyphs imported from other fonts will have colors
        psfsetmarkcolors -x $ufo

        echo "setting family ${f} and style ${s} in UFO ${ufo}"
        psfsetkeys -p backup=0 -k familyName                         -v "${f}" $ufo
        psfsetkeys -p backup=0 -k openTypeNamePreferredFamilyName    -v "${f}" $ufo
        psfsetkeys -p backup=0 -k styleName                          -v "${s}" $ufo
        psfsetkeys -p backup=0 -k openTypeNamePreferredSubfamilyName -v "${s}" $ufo
        psfsetkeys -p backup=0 -k postscriptFullName                 -v "${f} ${s}" $ufo
        psfsetkeys -p backup=0 -k styleMapFamilyName                 -v "${f}" $ufo
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
        if [ -f rename-${f}.csv ]
        then
            echo "renaming glyphs in UFO ${ufo}"
            psfrenameglyphs -i rename-${f}.csv $ufo
        fi
        if [ -f composites.txt ]
        then
            echo "building composites in UFO ${ufo}"
            psfbuildcomp -c -i composites.txt $ufo
        fi

        # echo "polishing glyphs in UFO ${ufo}"
        ${nlci}/polish.py $ufo

        if [ -x ../tools/cleanup.py ]
        then
            echo "fixing glyphs in UFO ${ufo}"
            ../tools/cleanup.py $ufo
        fi
        if [ -x ../tools/anchors.bash ]
        then
            echo "Preparing to add (adjust) anchors in UFO ${ufo}"
            ../tools/anchors.bash $ufo
        fi
        if [ -x ../tools/anchors.py ]
        then
            ../tools/anchors.py $ufo
        fi
        if [ "$s" = "Regular" ]
        then
            echo "listing glyphs in UFO ${ufo}"
            options=""
            if [ -f languages.csv ]
            then
                options="$options --langs languages.csv"
            fi
            if [ -f features.csv ]
            then
                options="$options --feats features.csv"
            fi
            ${nlci}/ufo2glyphdata.py $options $HOME/script/adobe/agl-aglfn/aglfn.txt $ufo glyph_data-${f}.csv
        else
            italic_option=""
            if [ "$s" = "Italic" -o "$s" = "Bold Italic" ]
            then
                italic_option="-i"
                echo "fixing italicAngle in UFO ${ufo}"
                psfsetkeys -p backup=0 -k "italicAngle" -v "-12" $ufo
            fi
            ${nlci}/copyanchors.py $italic_option -l $nlci/anchors.json ${f}-Regular.ufo $ufo
        fi
    done
done

popd

echo "now running preflight"
./preflight
echo "done running preflight"
echo "done producing UFO sources"
