#!/bin/bash

# =============================================================================
#                       Jenkins Build/Test/Deploy Script
#
# This is a bash script to build, test and deploy Lambda Lovelace's backend.
# At the time of writing Jenkins is installed on our UCD virtual machine and is
# accessible at http://csi6220-1-vm1.ucd.ie:8080/ during the project if you got
# the right credentials.
#
# Every time there is a new push to our Git repository this script executes.
# First it builds a Docker image. Fires up a testing container and runs tests
# and if nothing failed images are pushed to Docker Hub and then finally the
# new "production" container is swapped.
#
# Notes:
#
#   1.
#   Before we deploy a new version we have to stop and remove the previous
#   Docker container. We normally name our containers and remove like this:
#
#       docker rm -f "name-of-container" || true
#
#   The "|| true" bit is a bit of a hack to satisfy Jenkins. When Jenkins runs
#   scripts it fails a build if any command or execution doesn't return 0
#   (successful execution). Docker returns an error if we try to remove a
#   container that doesn't exist. For us that's grand, we didn't want it
#   anyway! So the "or true" bit simply guarantees we return so the script can
#   continue executing.
#
#   2.
#   I try my best to explain what the various commands and flags do but if
#   something is missing then please refer to the official Docker docs at:
#   https://docs.docker.com/engine/reference/run/
#
# Author: Jón Rúnar Helgason, jonrh, 2016
# =============================================================================

# Move into the backend/ folder where our Docker image is located
cd backend

# =============================================================================
#                           VARIABLE DEFINITIONS
# =============================================================================
# Define a variable to hold a short version of the git commit this build
# represents. E.g: "c721cdd"
GITHASH=$(git rev-parse --short HEAD)

# Jenkins build numbers are incrementing integers (1,2,3,...) for each build.
# Prefix it with a J in case we switch to some other tool than Jenkins. That
# way we can prefix it with different letter so we can tell the Docker image
# tags apart. Example: J1337
JENKINS_BUILDNUMBER="J$BUILD_NUMBER"

# The name of the Docker image. The "lovelace" part is the user name on Docker
# Hub. "/backend" is the image repository. Text after : is a tag (version).
# Example: lovelace/backend:J1337
IMAGE_NAME="lovelace/backend:$JENKINS_BUILDNUMBER"

# Build a docker image with the name lovelace/backend and tag. The dot at the
# end is important. It means "and copy all the contents of my current working
# directory to the container". Since the script executes inside the backend/
# folder it basically means we shove all files and folders in the backend/
# folder into the container.
#
# Example image name: lovelace/backend:J1337 where 1337 is the build number
docker build -t $IMAGE_NAME .

# =============================================================================
#                                   TESTS
# =============================================================================
# Stop & remove the Docker container "backend-testing" if it exits
docker rm -f "backend-testing" || true
docker rm -f "backend-unittests" || true

# Start up a Docker container with the name "backend-testing". We don't need to
# map any ports because the tests will be run inside the container
docker run -d --name="backend-testing" $IMAGE_NAME

# This is a bit of a shit mix. The problem we were faced with was that in
# order to test a web service (by calling an endpoint) it needs to be up and
# running. My bash scripting foo isn't that good so the only way I found was
# to simply wait for 5 seconds then run the tests. Then the service would be
# up for sure.
sleep 5s

docker run --name "backend-unittests" --link "backend-testing" $IMAGE_NAME nosetests tests.py && docker logs "backend-testing"

# Execute the Python tests inside the testing container. The command
# "nosetests" is some testing tool I saw was popular. It claims to be "nicer"
# testing than the standard Python testing. I don't really see why. It claims
# to be in maintenance mode, then there is nosetests2 which claims to be a
# successor but at the time of writing it seems to be even less maintained.
# Long story short: I find it confusing and I have no reservation to switch to
# some other Python tester. See here: https://nose.readthedocs.io/en/latest/
#
# "usr/src/app/" is the path our source code gets shoved in the Docker
# container. This path is determined by the Python on-build docker image. If
# we switch to another base image we may have to update that string.
# See more here: https://hub.docker.com/_/python/
#docker exec "backend-testing" nosetests /usr/src/app/tests.py

# Print logs so that the Jenkins build console log has a record of if the
# server started normally. Easier debugging.
docker logs "backend-testing"

# Stop and delete the testing container, throw it away, we're done here!
docker rm -f "backend-testing"
docker rm -f "backend-unittests"

# =============================================================================
#                   DOCKER TAGGING AND PUSHING TO DOCKER HUB
# =============================================================================
# If we got to here the tests passed. Tag the Docker image we built with the
# tag latest as it's solid and ready to be pushed to Docker Hub.
docker tag $IMAGE_NAME "lovelace/backend:latest"

# Log in to Docker Hub with user and pass credentials
docker login -u lovelace -p sexymard

# Push to Docker Hub our new versions. They are the same so no duplicate upload
# happens. We push both so we always have an "latest" image so we don't have
# to look up the latest build number if we need to manually start a container.
docker push $IMAGE_NAME
docker push "lovelace/backend:latest"

# Python backend Flask web service container
# =============================================================================
# Stop and throw away the previously running backend container if it exits
docker rm -f "backend-running" || true

# Start and run the new container
#
# -p 80:80: map port 80 of the host to port 80 in the container
# -e: passes in environment variables. We use two, the Jenkins build number
#	  and the short Git hash of the latest commit. This is then used in the
#     root / endpoint in the Flask app, so we can easily see which version
#	  is being currently run. Example: http://csi6220-1-vm1.ucd.ie/
# -itd: Detached Interactive TTY terminal session. Generally we want to detach
#       our containers (so poor Jenkins doesn't drown in STDOUT). I'm not
#       quite sure what the -it part does, but it allows us to detach from
#       containers without killing them (by pressing Ctrl + P then Ctrl + Q
#       if we ever need to manually peek inside of them while debugging.
docker run --name="backend-running" -itd -p 80:80 --restart=on-failure:50 \
    -e JENKINS_BUILDNUMBER=$BUILD_NUMBER -e GITHASH=$GITHASH \
    $IMAGE_NAME \
    gunicorn -w 1 -b 0.0.0.0:80 --log-level debug Lovelace:app

# If the celery-redis container is not running: remove any remains and start
# up a new one. This is a message broker for the Celery worker, a queue.
if [ ! $(docker inspect -f "{{.State.Running}}" "celery-redis") ] ; then
    docker rm -f "celery-redis" || true
    docker run -itd --name "celery-redis" redis
fi

# Python Celery container
# =============================================================================
# Stop and throw away the previously running celery container if it exits
docker rm -f "celery-worker" || true

# Start a Celery worker container. It basically re-uses the backend container
# but starts it with an overwritten execution command:
#
#   celery -A tasks worker -B -c 8 --loglevel=info
#
# We do this because both share a lot of the same dependencies and it
# simplifies the build/test/deploy script quite a bit. Reuse for the win!
#
# Docker containers run as the root user by default. This poses a problem for
# Celery because it uses pickle which is insecure. -e C_FORCE_ROOT=True runs
# the container with an environment variable that allows us to run as root.
# It's not really ideal but it's an okay fix for us.
# See more here: http://stackoverflow.com/q/20346851
docker run --name="celery-worker" -itd -e C_FORCE_ROOT=True --link celery-redis $IMAGE_NAME celery -A tasks worker -B -c 8 --loglevel=info

# The Docker CLI program gave some issues with signing in multiple times. To
# fix it I simply log out after the build is complete and sign in again when
# the next build starts. In and out.
docker logout

# =============================================================================
#                                    ROLLBAR
# =============================================================================
# The code below sends a notification to Rollbar (our logging service) that
# a new deployment occurred. I don't have any idea what this all does, it's
# just a copy paste as instructed from Rollbar.
ACCESS_TOKEN=9a41d7e8fdbb49cead0cae434765a927
ENVIRONMENT=production
LOCAL_USERNAME=`whoami`
REVISION=`git log -n 1 --pretty=format:"%H"`

curl https://api.rollbar.com/api/1/deploy/ \
  -F access_token=$ACCESS_TOKEN \
  -F environment=$ENVIRONMENT \
  -F revision=$REVISION \
  -F local_username=$LOCAL_USERNAME