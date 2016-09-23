#!/usr/bin/env bash
set -e

find ./data/files -type f -exec sh -c 'test "$(head -c 4 "$1")" = "%PDF"' sh {} \; -print
