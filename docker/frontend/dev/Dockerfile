FROM node:20.11.1-alpine3.19@sha256:c0a3badbd8a0a760de903e00cedbca94588e609299820557e72cba2a53dbaa2c

WORKDIR /app
COPY ./frontend/package*.json /app/.
RUN npm ci
EXPOSE 3000

CMD ["npm", " run start"]
