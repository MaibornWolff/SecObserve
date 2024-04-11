FROM node:20.12.2-alpine3.19@sha256:3321ad83759c5bb1a18575b40606dee561bbdb6b2b008327c17d85adeb3939d1

WORKDIR /app
COPY ./frontend/package*.json /app/.
RUN npm ci
EXPOSE 3000

CMD ["npm", " run start"]
