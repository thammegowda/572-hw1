#!/usr/bin/env bash


#Uses http-server from npm
# For setup::
#   apt-get install npm nodejs-legacy
#   npm install http-server -g

echo "Serving files from $PWD"
http-server
