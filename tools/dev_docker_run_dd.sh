#!/usr/bin/env bash
set -ex

IMAGE=datadog/docker-dogstatsd
# IMAGE=datadog/docker-dd-agent

docker run -ti --rm \
  --name dogstatsd \
  -h `hostname` \
  -v /var/run/docker.sock:/var/run/docker.sock:ro \
  -e API_KEY=$DD_API_KEY \
  -e LOG_LEVEL=DEBUG \
  -e DD_LOG_LEVEL=DEBUG \
  -e TAGS="env:development" \
  -p 8125:8125/udp \
  $IMAGE
