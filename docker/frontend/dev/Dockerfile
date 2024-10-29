FROM node:22.10.0-alpine3.20@sha256:fc95a044b87e95507c60c1f8c829e5d98ddf46401034932499db370c494ef0ff AS build

WORKDIR /app
COPY ./frontend/package*.json /app/.
RUN npm ci
EXPOSE 3000

CMD ["npm", " run start"]
