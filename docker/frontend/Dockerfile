# build environment
FROM node:18.16.0-alpine as build

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
FROM nginxinc/nginx-unprivileged:stable-alpine

USER root

RUN apk del curl && \
        apk add --no-cache --virtual --update nodejs npm && \
        npm i -g runtime-env-cra@0.2.4

COPY --from=build /app/build /usr/share/nginx/html
COPY ./frontend/.env.example /usr/share/nginx/html/.env
COPY ./frontend/nginx/nginx.conf /etc/nginx/conf.d/default.conf

ARG user=nginx
ARG group=nginx

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
