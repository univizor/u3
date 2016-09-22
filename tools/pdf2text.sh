#!/usr/bin/env bash
set -ex

echo "THIS IS EXPERIMENTAL."

PDF_FILE=./data/files/full/0a2fa2e43ee6a1fdd9738044e74604970d7e83bb.pdf

gs -sDEVICE=txtwrite \
  -dFirstPage=1 -dLastPage=1 \
  -dNODISPLAY -dNOPAUSE -dBATCH -dSAFER -dWRITESYSTEMDICT -dSIMPLE -dDELAYBIND\
  -sOutputFile=test.txt $PDF_FILE