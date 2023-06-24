FROM python:3.11.4-alpine as python

# Python build stage
FROM python as python-build-stage

ARG BUILD_ENVIRONMENT=prod

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
ARG VERSION=unkown

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV BUILD_ENV ${BUILD_ENVIRONMENT}

WORKDIR ${APP_HOME}

# Add user and group to avoid running as roolt
ARG user=django
ARG group=django

# All absolute dir copies ignore workdir instruction. All relative dir copies are wrt to the workdir instruction
# copy python dependency wheels from python-build-stage
COPY --from=python-build-stage /usr/src/app/wheels  /wheels/

# copy startup scripts
COPY ./docker/backend/prod/django/entrypoint /entrypoint
COPY ./docker/backend/prod/django/start /start
COPY ./docker/backend/prod/django/wait-for-it.sh /wait-for-it.sh

# copy application code to WORKDIR
COPY ./backend ${APP_HOME}

# use prod settings
COPY ./backend/config/settings/prod.py ${APP_HOME}/config/settings/dist.py

# certificate for MS Azure managed MySQL database
COPY ./docker/backend/prod/database/BaltimoreCyberTrustRoot_combined.crt.pem ${APP_HOME}/BaltimoreCyberTrustRoot_combined.crt.pem

RUN addgroup -g 1001 -S ${group} \
    && adduser -u 1001 -S ${user} -G ${group} \
    # Install binaries and libs for PostgreSQL
    && apk add --no-cache --virtual postgresql-libs postgresql-client mariadb-dev mysql-client bash \
    # use wheels to install python dependencies
    && pip install --no-cache-dir --no-index --find-links=/wheels/ /wheels/* \
    && rm -rf /wheels/ \
    # make startup scripts executable
    && chmod +x /entrypoint \
    && chmod +x /start \
    && chmod +x /wait-for-it.sh \
    # insert version for status endpoint
    && sed -i 's/version_unkown/'"${VERSION}"'/g' ${APP_HOME}/application/commons/api/views.py \
    # make staticfiles writeable 
    && mkdir ${APP_HOME}/application/staticfiles \
    && chmod ugo+w ${APP_HOME}/application/staticfiles \
    # create directory for huey task queue
    && mkdir /var/lib/huey \
    && chown -R ${user}:${group} /var/lib/huey \
    && chmod ugo+rw /var/lib/huey

HEALTHCHECK --interval=30s --timeout=30s --start-period=30s --retries=3 \
    CMD wget -nv -t1 --spider 'http://localhost:5000/api/status/health/' || exit 1

EXPOSE 5000

USER ${user}

ENTRYPOINT ["/entrypoint"]
