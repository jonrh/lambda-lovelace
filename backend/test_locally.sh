#!/bin/bash

# =============================================================================
#
#
# Author: Jón Rúnar Helgason, jonrh, 2016
# =============================================================================

cd backend/
docker build -t "test_image" .

docker rm -f "backend-testing"
docker run -d --name="backend-testing" "test_image"

sleep 5s

docker run --name "test-unittests" --link "backend-testing" --rm "test_image" nosetests tests.py || { docker logs "backend-testing"; exit 1; }
