#!/usr/bin/env bash
set -ex

docker run -ti --rm \
  --name dogstatsd \
  -h `hostname` \
  -e API_KEY=$DD_API_KEY \
  datadog/docker-dogstatsd
