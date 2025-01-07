FROM node:22.12.0-alpine@sha256:b09589de497084c656bb7f05078860793d1dffc019bfd1d733cdc1404bff3d1e AS build

WORKDIR /app
COPY ./frontend/package*.json /app/.
RUN npm ci
EXPOSE 3000

CMD ["npm", " run start"]
