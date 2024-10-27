#!/bin/bash

# Load the env vars from .env
export $(grep -v '^#' .env | xargs)

docker build \
  --build-arg URL=$URL \
  --build-arg STORE_PAGE1=$STORE_PAGE1 \
  --build-arg STORE_PAGE2=$STORE_PAGE2 \
  --build-arg STORE_PAGE3=$STORE_PAGE3 \
  --build-arg STORE_PAGE4=$STORE_PAGE4 \
  --build-arg STORE_PAGE5=$STORE_PAGE5 \
  -t patrick-star:v2 .
