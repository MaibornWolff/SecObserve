FROM node:20.14.0-alpine3.19@sha256:db6fa523bc20b4e4448bc77a9d8ff31e00ffbe511f83f7603abb438aa151bf7d

WORKDIR /app
COPY ./frontend/package*.json /app/.
RUN npm ci
EXPOSE 3000

CMD ["npm", " run start"]
