#!/bin/bash

echo HTTP_PROXY=$http_proxy
echo HTTP_PROXY=$https_proxy
docker build --build-arg HTTP_PROXY=$http_proxy --build-arg HTTPS_PROXY=$https_proxy -t xjimmyshcn/fastapi-web-starter:20211130 .
