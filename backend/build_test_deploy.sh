#!/bin/bash

# Move into the backend/ folder where our Docker image is located
cd backend

# Variable definitions:
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

# Build a docker image with the name lovelace/backend and tag.
# Example: lovelace/backend:J1337 where 1337 is the build number
docker build -t $IMAGE_NAME .

# =============================================================================
#                                   TESTS
# =============================================================================
#docker run $IMAGE_NAME nosetests tests.py

docker rm -f "backend-testing" || true
docker run --name="backend-testing" -p 1337:80 --detach $IMAGE_NAME
sleep 5s
docker exec "backend-testing" nosetests /usr/src/app/tests.py
docker rm -f "backend-testing"

# Tag the image we built with the tag latest
docker tag $IMAGE_NAME "lovelace/backend:latest"

# Log in to Docker Hub with user and pass credentials
docker login -u lovelace -p sexymard

# Push to Docker Hub our new versions. They are the same so duplicate upload
# happens. We push both so we always have an "latest" image so we don't have
# to look up the latest build number if we need to manually start a container.
docker push $IMAGE_NAME
docker push "lovelace/backend:latest"

# Remove the previous container if it was running. The "|| true" bit is to
# have the build not fail if the container didn't exist. Note that for this
# script we always name our running backend container "backend-running". This
# is more of a dirty hack. The alternative would be to name it with for
# example Jenkins build number but I'm not smart enough to look it up to shut
# down a previous container.
docker rm -f backend-running || true

# Start and run the new container
# + give the container the name "backend-running"
# + -p 80:80: map port 80 of the host to port 80 in the container
# + -e: passes in environment variables. We use two, the Jenkins build number
#		and the short Git hash of the latest commit. This is then used in the
#		root / endpoint in the Flask app, so we can easily see which version
#		is being currently run. Example: http://csi6220-1-vm1.ucd.ie/
# + --detach: runs the container in a background process, i.e. doesn't attach
#			  to the stdin/out
docker run --name="backend-running" -p 80:80 -e JENKINS_BUILDNUMBER=$BUILD_NUMBER -e GITHASH=$GITHASH --detach --restart=on-failure:50 $IMAGE_NAME

# The Docker CLI program gave some issues with signing in multiple times. To
# fix it I simply log out after the build is complete and sign in again when
# the next build starts. In and out.
docker logout

# The code below sends a notification to Rollbar (our logging service) that
# a new deployment ocurred. I don't have any idea what this all does, it's
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