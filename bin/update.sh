#!/bin/sh

set -e

cd /home/idch-fastapi-inference/app
echo "Updating code..."
git fetch origin
git reset --hard origin/master

echo "Building new images..."
docker compose -f docker-compose.prod.yaml build

echo "Deploying with rolling update..."
docker compose -f docker-compose.prod.yaml up -d --no-deps --build

echo "Deployment successful"
