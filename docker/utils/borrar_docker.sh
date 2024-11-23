docker stop $(docker ps -aq)
docker network prune
docker rm $(docker ps -aq)
docker rmi $(docker images -aq)

