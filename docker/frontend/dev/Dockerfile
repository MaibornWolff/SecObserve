FROM node:20.18.0-alpine3.19@sha256:2d8c24d9104bda27e07dced6d7110aa728dd917dde8255d8af3678e532b339d6

WORKDIR /app
COPY ./frontend/package*.json /app/.
RUN npm ci
EXPOSE 3000

CMD ["npm", " run start"]
