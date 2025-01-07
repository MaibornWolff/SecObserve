FROM node:22.12.0-alpine@sha256:4a5468a23354839a70381edc2d44edd79d9de678914b86ecf176ead1f1169c22 AS build

WORKDIR /app
COPY ./frontend/package*.json /app/.
RUN npm ci
EXPOSE 3000

CMD ["npm", " run start"]
