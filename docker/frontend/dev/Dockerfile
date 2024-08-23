FROM node:20.17.0-alpine3.19@sha256:61e2d8da651b86774b20f244e44a5a796bb70c6b3021aa62db4f78127c906d9b

WORKDIR /app
COPY ./frontend/package*.json /app/.
RUN npm ci
EXPOSE 3000

CMD ["npm", " run start"]
