# Installation

## Docker Compose

SecObserve provides 2 Docker Compose files as templates for productive use: `docker-compose-prod-mysql.yml` and `docker-compose-prod-postgres.yml`. Both start [Traefik](https://doc.traefik.io/traefik/v3.0/) as an edge router as well as the SecObserve frontend and backend plus a database (either MySQL or PostgreSQL).

Without any changes to the Docker Compose file, 3 URL's are available:

* **Frontend**: [http://secobserve.localhost](http://secobserve.localhost)
* **Backend**: [http://secobserve-backend.localhost](http://secobserve-backend.localhost) (base URL)
* **Traefik**: [http://traefik.localhost](http://traefik.localhost) (dashboard)


```include {language=yaml title="docker-compose-prod-postgres.yml"}
docker-compose-prod-postgres.yml
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
