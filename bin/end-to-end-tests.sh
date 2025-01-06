#!/bin/sh

docker compose -f docker-compose-playwright.yml up --build --abort-on-container-exit --exit-code-from playwright
