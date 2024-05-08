FROM node:20.13.0-alpine3.19@sha256:fac6f741d51194c175c517f66bc3125588313327ad7e0ecd673e161e4fa807f3

WORKDIR /app
COPY ./frontend/package*.json /app/.
RUN npm ci
EXPOSE 3000

CMD ["npm", " run start"]
