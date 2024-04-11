FROM node:20.12.2-alpine3.19@sha256:b0ff0ebeb3b98eced8c804ff184003faeaacfafe5021224e0f880cdaaff4e4f9

WORKDIR /app
COPY ./frontend/package*.json /app/.
RUN npm ci
EXPOSE 3000

CMD ["npm", " run start"]
