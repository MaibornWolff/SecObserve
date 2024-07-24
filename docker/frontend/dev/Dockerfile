FROM node:20.15.1-alpine3.19@sha256:94f0e02505b6e29bcdf363e512b35dd0bfb759ed04b2bb401874d0a95b16c4e9

WORKDIR /app
COPY ./frontend/package*.json /app/.
RUN npm ci
EXPOSE 3000

CMD ["npm", " run start"]
