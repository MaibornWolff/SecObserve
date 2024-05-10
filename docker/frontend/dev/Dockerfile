FROM node:20.13.1-alpine3.19@sha256:291e84d956f1aff38454bbd3da38941461ad569a185c20aa289f71f37ea08e23

WORKDIR /app
COPY ./frontend/package*.json /app/.
RUN npm ci
EXPOSE 3000

CMD ["npm", " run start"]
