FROM node:22.12.0-alpine3.20@sha256:60ed91cb8b3d78a7832700f89162667f65bd8ad715b446bd6b243f3397bc8292 AS build

WORKDIR /app
COPY ./frontend/package*.json /app/.
RUN npm ci
EXPOSE 3000

CMD ["npm", " run start"]
