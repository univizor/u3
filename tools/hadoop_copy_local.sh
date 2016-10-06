#!/usr/bin/env bash
set -e

# Copies local file to hadoop FS

find data/files -type f -exec hadoop fs -copyFromLocal -f {} /user/hadadmin/data/files \;
