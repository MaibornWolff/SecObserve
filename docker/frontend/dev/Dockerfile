FROM node:22.11.0-alpine3.20@sha256:f265794478aa0b1a23d85a492c8311ed795bc527c3fe7e43453b3c872dcd71a3 AS build

WORKDIR /app
COPY ./frontend/package*.json /app/.
RUN npm ci
EXPOSE 3000

CMD ["npm", " run start"]
