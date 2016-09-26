#!/usr/bin/env bash
set -e

#gs -sDEVICE=txtwrite -dFirstPage=1 -dLastPage=1 -dNOPAUSE -dBATCH -sOutputFile=- -f ./data/files/full/12fb11c0ef46370715489784d3047fe9255b99cd.pdf
#find ./data/files/full -name '*.pdf' | parallel --progress -j 5 \
#  'gs -q -sDEVICE=txtwrite -dFirstPage=1 -dLastPage=1 -dNOPAUSE -dBATCH -dSIMPLE -o {}.txt {}'


declare -a types=("diplomsko" "magistrsko" "doktorska" "projekt")
#for i in "${types[@]}"; do
##  documents=`grep -lir $i ./data/first-pages | wc -l`
#  echo $i $documents
#done

#find ./data/files -type f -exec 'gs -sDEVICE=txtwrite -dFirstPage=1 -dLastPage=1 -dNOPAUSE -dBATCH dSIMPLE -sOutputFile=- -f {}'
#find ./data/files -type f -exec sh -c 'test "$(head -c 4 "$1")" != "%PDF"' sh {} \; -print
#find ./data/files -type f -exec sh -c 'gs -sDEVICE=txtwrite -dFirstPage=1 -dLastPage=1 -dNOPAUSE -dBATCH dSIMPLE -sOutputFile=- -f $1' \;
# sh {} \; -print
#  -type f
#find ./data/files -exec \
#  'gs -q -sDEVICE=txtwrite -dFirstPage=1 -dLastPage=1 -dNOPAUSE -dBATCH -dSAFER -ddSIMPLE -r150 -sOutputFile=- -f {}' \;
#

find ./data/files -type f -exec sh -c \
  'gs -q -sDEVICE=txtwrite -dFirstPage=1 -dLastPage=1 -dNOPAUSE -dBATCH -dSAFER -dSIMPLE -sOutputFile=- -f $1' sh {} \; -print
