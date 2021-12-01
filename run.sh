#!/bin/bash

# usage: bash -E ./run.sh

echo http_proxy=$http_proxy
echo https_proxy=$https_proxy
echo DEV_MODE=$dev_mode

docker run -d  --name fastapi-web-starter -p 8080:8080 \
  -e http_proxy=$http_proxy -e https_proxy=$https_proxy \
  -e DEV_MODE=$dev_mode \
  -v $PWD/.env:/fastapi-web-starter/.env xjimmyshcn/fastapi-web-starter:20211130
