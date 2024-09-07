FROM node:20.17.0-alpine3.19@sha256:4c92ca00cdebe1067ff9baf299eb51d44c10cb28f54cf83cd2f1ef037cdc8a9d

WORKDIR /app
COPY ./frontend/package*.json /app/.
RUN npm ci
EXPOSE 3000

CMD ["npm", " run start"]
