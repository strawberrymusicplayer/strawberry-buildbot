#!/bin/sh

sudo docker-compose down
sudo docker rm $(sudo docker ps -aq)
sudo docker rmi $(sudo docker images -q)
sudo docker volume rm $(sudo docker volume ls -qf dangling=true)
