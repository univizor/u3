#!/usr/bin/env bash
set -e

DATABASE_URL="postgresql://postgres:@pg:5432/u3_dev"
IMAGE=univizor/u3

rm -rf ./data/files-dev/*

docker run -ti --rm --name u3 --link pg \
  --env DATABASE_URL=$DATABASE_URL \
  --entrypoint "python" \
  $IMAGE "./recreate_database.py"

docker run -ti \
  --rm \
  --name u3 \
  -v `pwd`:/home/u3 \
  -v `pwd`/data/files-dev:/home/u3/data/files \
  --link pg \
  --link dogstatsd \
  --env DATABASE_URL=$DATABASE_URL \
  --env DOWNLOAD_DELAY=1 \
  $IMAGE $@