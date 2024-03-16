FROM node:20.11.1-alpine3.19@sha256:842159a809c86c28a799b235f95e6010aa64d967d98eee0db4db5979d33dd43e

WORKDIR /app
COPY ./frontend/package*.json /app/.
RUN npm ci
EXPOSE 3000

CMD ["npm", " run start"]
