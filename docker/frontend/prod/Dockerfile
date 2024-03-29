# build environment
FROM node:20.12.0-alpine3.19@sha256:ef3f47741e161900ddd07addcaca7e76534a9205e4cd73b2ed091ba339004a75 as build

ARG VERSION=unkown

WORKDIR /app
ENV PATH /app/node_modules/.bin:$PATH
COPY frontend/package.json ./
COPY frontend/package-lock.json ./
COPY frontend/.npmrc ./


RUN npm ci
COPY ./frontend ./
# insert version for status endpoint
RUN sed -i 's/version_unkown/'"${VERSION}"'/g' ./src/commons/about/About.tsx

RUN npm run build

# production environment
FROM nginxinc/nginx-unprivileged:stable-alpine3.18@sha256:cb01bbd6dd88f5d22617ebafb6e0bf23cef2633af914fd67f09ef278d0652661

USER root

# kics-scan ignore-block
# versions of dependencies from distribution are ok
RUN apk del curl && \
        apk add --no-cache --virtual --update npm && \
        npm i -g runtime-env-cra@0.2.4

COPY --from=build /app/build /usr/share/nginx/html
COPY ./frontend/.env.no_oidc /usr/share/nginx/html/.env
COPY ./frontend/nginx/nginx.conf /etc/nginx/conf.d/default.conf

ARG user=nginx
ARG group=nginx
ARG VERSION=unkown
ARG CREATED
ARG REVISION

# We want to overwrite what's coming from the base image
LABEL maintainer="stefan.fleckenstein@maibornwolff.de"

LABEL org.opencontainers.image.authors="stefan.fleckenstein@maibornwolff.de"
LABEL org.opencontainers.image.created=${CREATED}
LABEL org.opencontainers.image.description="SecObserve is an open source vulnerability management system for software development and cloud environments."
LABEL org.opencontainers.image.documentation="https://maibornwolff.github.io/SecObserve"
LABEL org.opencontainers.image.licenses="BSD3-Clause"
LABEL org.opencontainers.image.revision=${REVISION}
LABEL org.opencontainers.image.source="https://github.com/MaibornWolff/SecObserve"
LABEL org.opencontainers.image.title="SecObserve frontend"
LABEL org.opencontainers.image.url="https://github.com/MaibornWolff/SecObserve"
LABEL org.opencontainers.image.vendor="MaibornWolff GmbH"
LABEL org.opencontainers.image.version=${VERSION}

RUN chown -R ${user}:${group} /usr/share/nginx/html && \
        chmod -R 777 /usr/share/nginx/html && \
        chown -R ${user}:${group} /var/cache/nginx && \
        chown -R ${user}:${group} /var/log/nginx && \
        chown -R ${user}:${group} /etc/nginx/conf.d && \
        touch /var/run/nginx.pid && \
        chown -R ${user}:${group} /var/run/nginx.pid

HEALTHCHECK --interval=30s --timeout=30s --start-period=10s --retries=3 \
    CMD wget -nv -t1 --spider 'http://localhost:3000/#/login' || exit 1

EXPOSE 3000

WORKDIR /usr/share/nginx/html

USER ${user}

CMD ["/bin/sh", "-c", "runtime-env-cra && nginx -g \"daemon off;\""]
