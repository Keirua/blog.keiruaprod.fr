
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