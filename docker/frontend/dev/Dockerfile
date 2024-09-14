FROM node:20.17.0-alpine3.19@sha256:20b236009deb4c33bf7e255c32fe1e82da7eb0a10245657e0a6a846851fde521

WORKDIR /app
COPY ./frontend/package*.json /app/.
RUN npm ci
EXPOSE 3000

CMD ["npm", " run start"]
