#!/usr/bin/env bash
set -e

find ./data/files | parallel --progress -j 2 "./tools/hadoop_add_document.sh {}"
