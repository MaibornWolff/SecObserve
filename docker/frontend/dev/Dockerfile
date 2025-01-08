FROM node:22.13.0-alpine@sha256:7f2d161e6c2cd1be488cdd0e7dbcef4db5fe2925b8b2675f28eec0a6922ec206 AS build

WORKDIR /app
COPY ./frontend/package*.json /app/.
RUN npm ci
EXPOSE 3000

CMD ["npm", " run start"]
