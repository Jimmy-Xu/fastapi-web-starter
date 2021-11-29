#!/bin/bash

export http_proxy=http://192.168.3.2:8118

docker build --build-arg HTTP_PROXY=$http_proxy --build-arg HTTPS_PROXY=$http_proxy -t xjimmyshcn/fastapi-web-starter:20211130 .

