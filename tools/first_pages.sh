#!/usr/bin/env bash
set -ex

find ./data/files/full -name '*.pdf' | parallel --verbose --progress -j 4 \
  'gs -q -sDEVICE=jpeg -dFirstPage=1 -dLastPage=1 -dNOPAUSE -dBATCH -r500x500 -o {}.jpeg {}'
