#!/bin/sh

set -xe

NAME=devmeetings-discord-bot
docker build -t $NAME .
docker stop $NAME || true
docker rm $NAME || true
docker run -d --name $NAME -t $NAME 

