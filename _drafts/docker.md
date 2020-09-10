
Multiple databases ?
https://dev.to/bgord/multiple-postgres-databases-in-a-single-docker-container-417l

# build everything
docker-compose -f docker-compose.dev.yml build
# Building a container
docker-compose -f docker-compose.dev.yml build web

# starting/stopping 

docker-compose -f docker-compose.dev.yml up -d
docker-compose -f docker-compose.dev.yml up -d --force-recreate  --remove-orphans web
docker-compose -f docker-compose.dev.yml down

# Updating gems

docker-compose stop web
docker-compose build web
docker-compose up -d --force-recreate web

# Accessing logs 

    # single container:
    docker-compose -f docker-compose.dev.yml logs db
    # all the logs:
    docker-compose -f docker-compose.dev.yml logs -f

# Setting up the database

docker-compose run --rm web rails db:drop
docker-compose run --rm web rails db:create
docker-compose run --rm web rails db:migrate
docker-compose run --rm web rails test


# Connecting from a separate container

docker-compose -f docker-compose.dev.yml run --rm database psql -d jsp_test -U jsp_user_test -h database
docker-compose -f docker-compose.dev.yml run --rm web rails c

docker-compose -f docker-compose.dev.yml run --rm web /bin/sh

docker-compose -f docker-compose.dev.yml run --rm web rails db:create
docker-compose -f docker-compose.dev.yml run --rm web rails db:migrate
docker-compose -f docker-compose.dev.yml run --rm web rails assets:precompile

# you may need to set the owners occasionnally:
sudo sudo chown clemk:clemk -R tmp


# Docker-machine

It is possible to deploy a production-like environment using docker-machine, inside a virtualbox VM

First, we need to install docker-machine:
https://docs.docker.com/machine/install-machine/

Then, we can create our VM:

docker-machine rm local-vm-1
docker-machine create --driver virtualbox local-vm-1
docker-machine ls
docker-machine ssh local-env-1 (then 'exit', or ctrl-D to exit)
docker-machine ssh local-vm-1 "docker -v"

Then, we cana configure our local docker cli tool to be able to communicate with the VM directly:

    docker-machine env local-vm-1
    eval $(docker-machine env local-vm-1)

Now, all our docker commands will be run (from this terminal) inside this VM.

    docker-machine ls

