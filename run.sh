#!/bin/sh

set -xe

NAME=devmeetings-discord-bot
docker build -t $NAME .
docker run -t $NAME

