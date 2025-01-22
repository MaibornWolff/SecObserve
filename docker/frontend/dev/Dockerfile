FROM node:22.13.1-alpine@sha256:7f0fd7ed3746c496e40defda2ff51abc7de6cdb7dde304a649b8fbb3d152cf33 AS build

WORKDIR /app
COPY ./frontend/package*.json /app/.
RUN npm ci
EXPOSE 3000

CMD ["npm", " run start"]
