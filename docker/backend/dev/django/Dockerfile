FROM python:3.11.6-alpine as python

# Python build stage
FROM python as python-build-stage

ARG BUILD_ENVIRONMENT=dev

# Install packages
# kics-scan ignore-block
# versions of dependencies from distribution are ok
RUN apk add --no-cache --virtual .build-deps \
    ca-certificates gcc postgresql-dev linux-headers musl-dev libffi-dev mariadb-dev

# Requirements are installed here to ensure they will be cached.
COPY ./backend/requirements .

# Create Python Dependency and Sub-Dependency Wheels.
RUN pip wheel --wheel-dir /usr/src/app/wheels -r ${BUILD_ENVIRONMENT}.txt


# Python 'run' stage
FROM python as python-run-stage

ARG BUILD_ENVIRONMENT=dev
ARG APP_HOME=/app
ARG COMMIT_ID=undefined

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV BUILD_ENV ${BUILD_ENVIRONMENT}

WORKDIR ${APP_HOME}

# Add user and group to avoid running as root
ARG user=django
ARG group=django

# Install binaries and libs for PostgreSQL
# kics-scan ignore-block
# versions of dependencies from distribution are ok
RUN apk add --no-cache --virtual postgresql-libs postgresql-client mariadb-dev mysql-client bash

# use wheels to install python dependencies
COPY --from=python-build-stage /usr/src/app/wheels  /wheels/
RUN pip install --no-cache-dir --no-index --find-links=/wheels/ /wheels/* \
    && rm -rf /wheels/ && rm -rf /tmp

# copy startup scripts
COPY ./docker/backend/dev/django/entrypoint /entrypoint
COPY ./docker/backend/dev/django/start /start
COPY ./docker/backend/dev/django/wait-for-it.sh /wait-for-it.sh

# copy application code to WORKDIR
COPY ./backend ${APP_HOME}
# use dev settings
COPY ./backend/config/settings/dev.py ${APP_HOME}/config/settings/dist.py

RUN addgroup -g 1001 -S ${group} \
    && adduser -u 1001 -S ${user} -G ${group} \
    # make startup scripts executable
    && chmod +x /entrypoint \
    && chmod +x /start \
    && chmod +x /wait-for-it.sh \
    # insert commit id for status endpoint
    && sed -i 's/placeholder/'"${COMMIT_ID}"'/g' ${APP_HOME}/application/commons/api/views.py \
    # create directory for huey task queue
    && mkdir /var/lib/huey \
    && chown -R ${user}:${group} /var/lib/huey \
    && chmod ugo+rw /var/lib/huey


HEALTHCHECK --interval=30s --timeout=30s --start-period=10s --retries=3 \
    CMD wget -nv -t1 --spider 'http://localhost:8000/api/status/health/' || exit 1

USER ${user}

ENTRYPOINT ["/entrypoint"]
