#!/usr/bin/env bash
set -ex

# psql -U postgres u3_dev -c "DELETE FROM sources s WHERE s.domain = 'repozitorij.uni-lj.si';"

# ls ./data/files-rul/
# rm -rf ./data/files-rul/*

level=INFO

scrapy crawl rul -a mode=refresh -a pages=3 # -L $level