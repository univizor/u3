#!/usr/bin/env bash
set -ex

JOBS_IN_PARALLEL=4
LOG_LEVEL=WARNING
MODE=refresh

COMMANDS=(
  "bf -a mode=$MODE -a categories=biologija -L $LOG_LEVEL"
  "bf -a mode=$MODE -a categories=gozdarstvo -L $LOG_LEVEL"
  "bf -a mode=$MODE -a categories=agronomija -L $LOG_LEVEL"
  "bf -a mode=$MODE -a categories=zootehnika -L $LOG_LEVEL"
  "bf -a mode=$MODE -a categories=krajinska-arhitektura -L $LOG_LEVEL"
  "bf -a mode=$MODE -a categories=lesarstvo -L $LOG_LEVEL"
  "bf -a mode=$MODE -a categories=mikrobiologija -L $LOG_LEVEL"
  "bf -a mode=$MODE -a categories=zivilstvo -L $LOG_LEVEL"
  "bf -a mode=$MODE -a categories=biotehnologija -L $LOG_LEVEL"
  "rul -a mode=$MODE -a pages=10 -L $LOG_LEVEL"
)

parallel --verbose --progress -j $JOBS_IN_PARALLEL --colsep ' ' scrapy crawl {.} ::: "${COMMANDS[@]}"
