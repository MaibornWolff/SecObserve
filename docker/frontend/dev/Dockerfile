FROM node:20.14.0-alpine3.19@sha256:3c2ff49f98c64489f0408a0b26390a03a08e26fee8692b79cc1d3df0b134eaa6

WORKDIR /app
COPY ./frontend/package*.json /app/.
RUN npm ci
EXPOSE 3000

CMD ["npm", " run start"]
