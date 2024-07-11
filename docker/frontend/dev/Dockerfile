FROM node:20.15.1-alpine3.19@sha256:97f02cbb1c8ef6eefcfb1b1f958c012362758972cf125a99c09bd18b26a716c9

WORKDIR /app
COPY ./frontend/package*.json /app/.
RUN npm ci
EXPOSE 3000

CMD ["npm", " run start"]
