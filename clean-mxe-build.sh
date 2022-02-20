#!/bin/sh
sudo docker-compose run worker-mingw make -C /persistent-data/mingw/mxe-debug/source clean
sudo docker-compose run worker-mingw make -C /persistent-data/mingw/mxe-release/source clean
