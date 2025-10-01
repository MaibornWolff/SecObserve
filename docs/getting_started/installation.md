# Installation

!!! warning

    Both provided installation options serve as templates for productive use only. Even though they can run *out of the box*, they will need proper configuration for the requirements of the environment they will be installed in. This includes additional hardening and security measures.


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

## Kubernetes

SecObserve provides a Helm chart as a template for productive use. The default values will work if the release name is `secobserve` and the frontend will be accessible with [https://secobserve.dev/](https://secobserve.dev/).

#### Database

The PostgreSQL database is provided by Bitnami's Helm chart. Bitnami doesn't provide updates for their free tier anymore, see [Upcoming changes to the Bitnami Catalog](https://github.com/bitnami/charts?tab=readme-ov-file#%EF%B8%8F-important-notice-upcoming-changes-to-the-bitnami-catalog) and the Docker image is pulled from the `bitnamilegacy` repository. 

This is ok to test the Kubernetes installation, but not suitable for production use. A productive environment has to use an update-to-date database, e.g. installed as an operator like [CloudNativePG](https://cloudnative-pg.io/) or a managed service of a cloud provider.

If the provided database is used and the chart is installed with a release name different from `secobserve`, all occurrences of `secobserve-postgresql` in the chart have to be changed to `<release_name>-postgresql`.

#### Secrets

Three values are read from a secret, which has to be set up manually before installing the chart:

* `ADMIN_PASSWORD`
* `DJANGO_SECRET_KEY`
* `FIELD_ENCRYPTION_KEY`

The command to setup the secret can look like this:

```
kubectl create secret generic secobserve-secrets \
    --namespace ... \
    --from-literal=password='...' \
    --from-literal=django_secret_key='...' \
    --from-literal=field_encryption_key='...'
```

See [Configuration](configuration.md#backend) for more information how to set these values.
