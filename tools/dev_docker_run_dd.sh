#!/usr/bin/env bash
set -ex

IMAGE=datadog/docker-dogstatsd
LOG_LEVEL=DEBUG
# IMAGE=datadog/docker-dd-agent

docker run -ti --rm \
  --name dogstatsd \
  -h `hostname` \
  -v /var/run/docker.sock:/var/run/docker.sock:ro \
  -e API_KEY=$DD_API_KEY \
  -e LOG_LEVEL=$LOG_LEVEL \
  -e DD_LOG_LEVEL=$LOG_LEVEL \
  -e TAGS="env:development" \
  -p 8125:8125/udp \
  $IMAGE
