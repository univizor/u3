#!/usr/bin/env bash
set -ex

find ./data/files/full -name '*.pdf' | parallel --progress -j 5 \
  'gs -q -sDEVICE=txtwrite -dFirstPage=1 -dLastPage=1 -dNOPAUSE -dBATCH -dSIMPLE -o {}.txt {}'
