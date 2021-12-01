#!/bin/bash

docker build --build-arg HTTP_PROXY=$http_proxy --build-arg HTTPS_PROXY=$https_proxy -t xjimmyshcn/fastapi-web-starter:20211130 .

