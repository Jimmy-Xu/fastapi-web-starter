#!/bin/bash

export http_proxy=http://192.168.3.2:8118
docker run -d  --name fastapi-web-starter -p 8080:8080 \
  -e http_proxy=$http_proxy -e https_proxy=$http_proxy \
  -v $PWD/.env:/fastapi-web-starter/.env xjimmyshcn/fastapi-web-starter:20211130
