FROM python:3.11.4-alpine as python

# Python build stage
FROM python as python-build-stage

ARG BUILD_ENVIRONMENT=unittests

# Install packages
RUN apk add --no-cache --virtual .build-deps \
    ca-certificates gcc postgresql-dev linux-headers musl-dev libffi-dev mariadb-dev
    # These 2 libraries would only be needed for the Pillow package
    # jpeg-dev zlib-dev

# Requirements are installed here to ensure they will be cached.
COPY ./backend/requirements .

# Create Python Dependency and Sub-Dependency Wheels.
RUN pip wheel --wheel-dir /usr/src/app/wheels -r ${BUILD_ENVIRONMENT}.txt


# Python 'run' stage
FROM python as python-run-stage

ARG BUILD_ENVIRONMENT=prod
ARG APP_HOME=/app
ARG VERSION=unittest_version

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV BUILD_ENV ${BUILD_ENVIRONMENT}

WORKDIR ${APP_HOME}

# Add user and group to avoid running as root
ARG user=django
ARG group=django

# All absolute dir copies ignore workdir instruction. All relative dir copies are wrt to the workdir instruction
# copy python dependency wheels from python-build-stage
COPY --from=python-build-stage /usr/src/app/wheels  /wheels/

# copy startup scripts
COPY ./docker/backend/unittests/django/entrypoint /entrypoint
COPY ./docker/backend/unittests/django/start /start

# copy application code to WORKDIR
COPY ./backend ${APP_HOME}
# use prod settings
COPY ./backend/config/settings/unittests.py ${APP_HOME}/config/settings/dist.py

# use wheels to install python dependencies
RUN pip install --no-cache-dir --no-index --find-links=/wheels/ /wheels/* \
    && rm -rf /wheels/

RUN addgroup -g 1001 -S ${group} \
    && adduser -u 1001 -S ${user} -G ${group} \
    # make startup scripts executable
    && chmod +x /entrypoint \
    && chmod +x /start \
    # insert commit id for status endpoint
    && sed -i 's/version_unkown/'"${VERSION}"'/g' ${APP_HOME}/application/commons/api/views.py \
    # make staticfiles writeable 
    && mkdir ${APP_HOME}/application/staticfiles \
    && chown ${user}.${group} ${APP_HOME}

USER ${user}

ENTRYPOINT ["/entrypoint"]
