#!/usr/bin/env bash


#Uses http-server from npm
# For setup::
#   apt-get install npm nodejs-legacy
#   npm install http-server -g

# Setup Alias host
#   add an entry '127.0.0.1  aliashost' to  /etc/hosts
# alias host is treated as external host to localhost

echo "Serving files from $PWD"
http-server
