#!/usr/bin/env bash
set -e

find ./data/files | parallel --progress -j 5 "./tools/hadoop_add_document.sh {}"