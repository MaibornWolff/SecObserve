FROM node:22.13.0-alpine@sha256:fce322c9655fe5dc0aac3215bddf35d9907f1a6f59f990c1acace34a669eb86d AS build

WORKDIR /app
COPY ./frontend/package*.json /app/.
RUN npm ci
EXPOSE 3000

CMD ["npm", " run start"]
