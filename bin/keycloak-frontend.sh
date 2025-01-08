#!/bin/sh

docker compose -f docker-compose-dev-keycloak.yml --profile frontend up --build  
