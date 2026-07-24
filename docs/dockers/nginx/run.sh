#!/bin/sh

docker run -d --name soelatam_proxy -p 80:80 --add-host=host.docker.internal:host-gateway -v ./soelatam.conf:/etc/nginx/conf.d/default.conf nginx