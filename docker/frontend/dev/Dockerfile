FROM node:20.14.0-alpine3.19@sha256:acedb9b82ab6964a04329bf543c1d4692fbc75d255048c1665db90ab5026f753

WORKDIR /app
COPY ./frontend/package*.json /app/.
RUN npm ci
EXPOSE 3000

CMD ["npm", " run start"]
