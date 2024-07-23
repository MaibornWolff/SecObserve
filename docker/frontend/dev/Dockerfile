FROM node:20.15.1-alpine3.19@sha256:9230bd6e797304f09fde7c9dabbdff9df3d97cb6dc87d02d529a5e3029aafba2

WORKDIR /app
COPY ./frontend/package*.json /app/.
RUN npm ci
EXPOSE 3000

CMD ["npm", " run start"]
