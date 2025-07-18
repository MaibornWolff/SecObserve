FROM python:3.12-alpine@sha256:9b8808206f4a956130546a32cbdd8633bc973b19db2923b7298e6f90cc26db08 AS python-base

# Python build stage
FROM python-base AS python-build-stage

ARG BUILD_ENVIRONMENT=unittests

# Install packages
# kics-scan ignore-block
# versions of dependencies from distribution are ok
RUN apk add --no-cache --virtual .build-deps \
    ca-certificates gcc libffi-dev linux-headers mariadb-dev musl-dev postgresql-dev

# install dependencies with poetry
COPY ./backend/poetry_requirements.txt ./
RUN pip install --no-cache -r ./poetry_requirements.txt

ENV POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
    POETRY_VIRTUALENVS_CREATE=1 \
    POETRY_CACHE_DIR=/tmp/poetry_cache

WORKDIR /

COPY backend/pyproject.toml backend/poetry.lock ./
RUN poetry install --extras "unittests" --no-root && rm -rf "$POETRY_CACHE_DIR"


# Python 'run' stage
FROM python-base AS python-run-stage

ENV SO_UNITTESTS=true

ARG BUILD_ENVIRONMENT=prod
ARG APP_HOME=/app
ARG VERSION=unittest_version

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV BUILD_ENV=${BUILD_ENVIRONMENT}

WORKDIR ${APP_HOME}

# copy dependencies from build stage
ENV VIRTUAL_ENV=/.venv \
    PATH="/.venv/bin:$PATH"
COPY --from=python-build-stage ${VIRTUAL_ENV} ${VIRTUAL_ENV}

# copy startup scripts
COPY ./docker/backend/unittests/django/entrypoint /entrypoint

# copy application code to WORKDIR
COPY ./backend ${APP_HOME}
# use prod settings
COPY ./backend/config/settings/unittests.py ${APP_HOME}/config/settings/dist.py

RUN chmod +x /entrypoint \
    # insert commit id for status endpoint
    && sed -i 's/version_unknown/'"${VERSION}"'/g' ${APP_HOME}/application/commons/api/views.py \
    # make staticfiles writeable
    && mkdir ${APP_HOME}/application/staticfiles \
    && chmod ugo+w ${APP_HOME} \
    # create directory for huey task queue
    && mkdir /var/lib/huey \
    # create directory for sqlite db
    && mkdir /var/lib/sqlite \
    && chmod ugo+rw /var/lib/sqlite

ENTRYPOINT ["/entrypoint"]
