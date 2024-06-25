FROM node:20.15.0-alpine3.19@sha256:c39be8a03811d866e0f5e18fcd2065a914931a3c0830b29403017db3def59d91

WORKDIR /app
COPY ./frontend/package*.json /app/.
RUN npm ci
EXPOSE 3000

CMD ["npm", " run start"]
