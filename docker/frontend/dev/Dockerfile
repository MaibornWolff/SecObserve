FROM node:20.16.0-alpine3.19@sha256:e0ea1e2299d3e4b214ba91a0c1b773f2369ba4ff39cb0b4d3000c2b72ee8334e

WORKDIR /app
COPY ./frontend/package*.json /app/.
RUN npm ci
EXPOSE 3000

CMD ["npm", " run start"]
