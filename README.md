:strawberry: Strawberry Buildbot
=======================

This repository contains Strawberry's buildbot instance running on http://buildbot.strawbs.net/

It contains the configration and Dockerfiles to build the master, volumes and workers.

Currently the master runs with Python 3, but all the workers use Python 2, I have not figured out how to fix the workers for Python 3.


Containers are built, started and stopped with docker-compose.

### Create the configuration:

    ./update_config.py


### Build the containers:

    sudo docker-compose build --no-cache --pull

(This may take hours depending on your machine).


### Start buildbot:

    sudo docker-compose up -d


The buildbot is accessible on http://localhost:8010/


### View the log:

    sudo docker-compose run --entrypoint cat master /persistent-data/master/twistd.log


### Rebuild and restart worker to update a distros packages:

    sudo docker-compose build --no-cache --pull worker-opensuse-tumbleweed
    sudo docker-compose up -d worker-opensuse-tumbleweed


### Cleanup everything:

Shutdown:

    sudo docker-compose down

Remove all containers:

    sudo docker rm $(sudo docker ps -aq)

Remove all images:

    sudo docker rmi $(sudo docker images -q)

Remove volume:

    sudo docker volume rm $(sudo docker volume ls -qf dangling=true)


The cmake toolchain files for cross-compiling for Windows are in config/dist.


The development builds for macOS is using Travis-CI and the configration is here:
https://github.com/jonaski/strawberry/blob/master/.travis.yml

