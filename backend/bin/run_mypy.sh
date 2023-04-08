#!/bin/sh

export USE_DOCKER=no
# --- Admin user
export ADMIN_USER=admin
export ADMIN_PASSWORD=admin
export ADMIN_EMAIL=admin@example.com
# --- Database ---
export DATABASE_ENGINE=django.db.backends.sqlite3
export DATABASE_HOST=dummy
export DATABASE_PORT=9999
export DATABASE_DB=dummy
export DATABASE_USER=dummy
export DATABASE_PASSWORD=dummy
# --- Security ---
export ALLOWED_HOSTS=localhost
export CORS_ALLOWED_ORIGINS=http://localhost:3000
export DJANGO_SECRET_KEY=NxYPEF5lNGgk3yonndjSbwP77uNJxOvfKTjF5aVBqsHktNlf1wfJHHvJ8iifk32r
export FIELD_ENCRYPTION_KEY=DtlkqVb3wlaVdJK_BU-3mB4wwuuf8xx8YNInajiJ7GU=
# --- Azure AD ---
export AAD_CLIENT_ID=dummy
export AAD_TENANT_ID=dummy

mypy application
