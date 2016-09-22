#!/usr/bin/env bash
set -ex

psql -U postgres u3_dev -c "DELETE FROM sources s WHERE s.domain = 'dk.um.si';"

# ls ./data/files-rul/
# rm -rf ./data/files-rul/*

level=WARNING

scrapy crawl dkum -a mode=refresh -a pages=100 -L $level