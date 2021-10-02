#!/bin/sh
#Download the client
sudo apt-get update -y
sudo apt-get install wireguard -y
#Fix possible missing dependencies
ln -s /usr/bin/resolvectl /usr/local/bin/resolvconf
sudo apt-get install resolvconf -y
