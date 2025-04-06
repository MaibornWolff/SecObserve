# Installation

## Docker Compose

SecObserve provides 2 Docker Compose files as templates for productive use: `docker-compose-prod-mysql.yml` and `docker-compose-prod-postgres.yml`. Both start [Traefik](https://doc.traefik.io/traefik/v3.0/) as an edge router as well as the SecObserve frontend and backend plus a database (either MySQL or PostgreSQL).

Without any changes to the Docker Compose file, 3 URL's are available:

* **Frontend**: [http://secobserve.localhost](http://secobserve.localhost)
* **Backend**: [http://secobserve-backend.localhost](http://secobserve-backend.localhost) (base URL)
* **Traefik**: [http://traefik.localhost](http://traefik.localhost) (dashboard)


``` yaml title="docker-compose-prod-postgres.yml"
volumes:
  prod_postgres_data:

networks:
  traefik:
  database:

services:

  traefik:
    image: "traefik:v3.0"
    container_name: "traefik"
    command:
      - "--log.level=INFO"
      - "--api.dashboard=true"
      - "--providers.docker=true"
      - "--providers.docker.exposedbydefault=false"
      - "--entrypoints.web.address=:80"
    labels:
      - "traefik.enable=true"
      # - "traefik.http.middlewares.traefik-ipallowlist.ipallowlist.sourcerange=172.18.0.1/24"
      # - "traefik.http.routers.api.middlewares=traefik-ipallowlist@docker"
      - "traefik.http.routers.api.entrypoints=web"
      - "traefik.http.routers.api.rule=Host(`traefik.localhost`)"
      - "traefik.http.routers.api.service=api@internal"
    ports:
      - "80:80"
    volumes:
      - "/var/run/docker.sock:/var/run/docker.sock:ro"
    networks:
      - default

  frontend:
    image: maibornwolff/secobserve-frontend:1.30.0
    labels:
      - "traefik.enable=true"
      - "traefik.http.routers.frontend.rule=Host(`secobserve.localhost`)"
      - "traefik.http.routers.frontend.entrypoints=web"
    environment:
      API_BASE_URL: ${SO_API_BASE_URL:-http://secobserve-backend.localhost/api}
      OIDC_ENABLE: ${SO_OIDC_ENABLE:-false}
      OIDC_AUTHORITY: ${SO_OIDC_AUTHORITY:-dummy}
      OIDC_CLIENT_ID: ${SO_OIDC_CLIENT_ID:-dummy}
      OIDC_REDIRECT_URI: ${SO_OIDC_REDIRECT_URI:-http://secobserve.localhost}
      OIDC_POST_LOGOUT_REDIRECT_URI: ${SO_OIDC_POST_LOGOUT_REDIRECT_URI:-http://secobserve.localhost}
      OIDC_SCOPE: ${SO_OIDC_SCOPE:-openid profile email}
    networks:
      - traefik

  backend:
    image: maibornwolff/secobserve-backend:1.30.0
    labels:
      - "traefik.enable=true"
      - "traefik.http.routers.backend.rule=Host(`secobserve-backend.localhost`)"
      - "traefik.http.routers.backend.entrypoints=web"
    depends_on:
      - postgres
    environment:
      # --- Admin user ---
      ADMIN_USER: ${SO_ADMIN_USER:-admin}
      ADMIN_PASSWORD: ${SO_ADMIN_PASSWORD:-admin}
      ADMIN_EMAIL: ${SO_ADMIN_EMAIL:-admin@example.com}
      # --- Database ---
      DATABASE_ENGINE: ${SO_DATABASE_ENGINE:-django.db.backends.postgresql}
      DATABASE_HOST: ${SO_DATABASE_HOST:-postgres}
      DATABASE_PORT: ${SO_DATABASE_PORT:-5432}
      DATABASE_DB: ${SO_DATABASE_DB:-secobserve}
      DATABASE_USER: ${SO_DATABASE_USER:-secobserve}
      DATABASE_PASSWORD: ${SO_DATABASE_PASSWORD:-secobserve}
      # --- Security ---
      ALLOWED_HOSTS: ${SO_ALLOWED_HOSTS:-secobserve-backend.localhost}
      CORS_ALLOWED_ORIGINS: ${SO_CORS_ALLOWED_ORIGINS:-http://secobserve.localhost}
      DJANGO_SECRET_KEY: ${SO_DJANGO_SECRET_KEY:-NxYPEF5lNGgk3yonndjSbwP77uNJxOvfKTjF5aVBqsHktNlf1wfJHHvJ8iifk32r}
      FIELD_ENCRYPTION_KEY: ${SO_FIELD_ENCRYPTION_KEY:-DtlkqVb3wlaVdJK_BU-3mB4wwuuf8xx8YNInajiJ7GU=}
      # --- OpenID Connect ---
      OIDC_AUTHORITY: ${SO_OIDC_AUTHORITY:-}
      OIDC_CLIENT_ID: ${SO_OIDC_CLIENT_ID:-}
      OIDC_USERNAME: ${SO_OIDC_USERNAME:-}
      OIDC_FIRST_NAME: ${SO_OIDC_FIRST_NAME:-}
      OIDC_LAST_NAME: ${SO_OIDC_LAST_NAME:-}
      OIDC_FULL_NAME: ${SO_OIDC_FULL_NAME:-}
      OIDC_EMAIL: ${SO_OIDC_EMAIL:-}
      OIDC_GROUPS: ${SO_OIDC_GROUPS:-}
    command: /start
    networks:
      - traefik
      - database

  postgres:
    image: postgres:15.2-alpine
    environment:
      POSTGRES_DB: ${SO_POSTGRES_DB:-secobserve}
      POSTGRES_USER: ${SO_POSTGRES_USER:-secobserve}
      POSTGRES_PASSWORD: ${SO_POSTGRES_PASSWORD:-secobserve}
    volumes:
      - prod_postgres_data:/var/lib/postgresql/data
    networks:
      - database
```

#### Configuration for Traefik

* The Traefik dashboard should either be configured with authentication or disabled, see [The Dashboard](https://doc.traefik.io/traefik/v3.0/operations/dashboard/).
* Encrypted communiction should be configured for frontend and backend. Traefik supports given certificates and automatic configuration with Let's Encrypt, see [HTTPS & TLS](https://doc.traefik.io/traefik/v3.0/https/overview/).

#### Configuration for SecObserve

The Docker Compose file sets default values for the SecObserve configuration, so that the containers can run out of the box. All default values can be overriden, by setting respective environment variables in the shell before starting Docker Compose. To avoid name collisions, the environment variables in the shell need to have a `SO_` prefix in front of the name as it is stated in [Configuration](configuration.md).

Some values should be changed for productive use, to avoid using the default values for secrets:

* `SO_ADMIN_PASSWORD`
* `SO_DATABASE_PASSWORD`
* `SO_DJANGO_SECRET_KEY`
* `SO_FIELD_ENCRYPTION_KEY`

#### Startup

* The database structure is initialized with the first start of the backend container.
* The URLs for frontend and backend are available after approximately 30 seconds, after the healthcheck of the containers has been running for the first time.
