FROM node:20.15.0-alpine3.19@sha256:1bdec9c67503d33348be6e73a8e5e94aad679b32da15e4fd3956e5e48f87f623

WORKDIR /app
COPY ./frontend/package*.json /app/.
RUN npm ci
EXPOSE 3000

CMD ["npm", " run start"]
