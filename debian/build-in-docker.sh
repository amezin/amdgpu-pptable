#!/bin/bash

mkdir -p ../dist/debian/src
docker-compose build
docker-compose run --user "$(id -u)" build "$@"
