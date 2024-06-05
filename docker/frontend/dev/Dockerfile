FROM node:20.14.0-alpine3.19@sha256:eb17a0816c6475000def8bf0dd0a85bc59340235eb9fbb0aff158b4c9a3c7d6f

WORKDIR /app
COPY ./frontend/package*.json /app/.
RUN npm ci
EXPOSE 3000

CMD ["npm", " run start"]
