FROM node:20.15.1-alpine3.19@sha256:9521a34b28f6f646672e20aad4b0dad4f26acbfca238c6242cf7c2e7583a200c

WORKDIR /app
COPY ./frontend/package*.json /app/.
RUN npm ci
EXPOSE 3000

CMD ["npm", " run start"]
