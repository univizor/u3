#!/usr/bin/env bash
set -ex

find data/files -type f -maxdepth 1 -iname "*.pdf" | tail -1000 | xargs -I{} cp -n {} ../cog/data/files/
