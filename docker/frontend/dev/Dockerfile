FROM node:20.14.0-alpine3.19@sha256:2d0ce60a5c7bfa2bcdcfa7d463d8f8b7b16cab55051562606a9dc32c8a8169a9

WORKDIR /app
COPY ./frontend/package*.json /app/.
RUN npm ci
EXPOSE 3000

CMD ["npm", " run start"]
