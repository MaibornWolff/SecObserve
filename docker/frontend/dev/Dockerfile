FROM node:22.13.0-alpine@sha256:784a600a1c686b3167785cf151c7164d44b99c3d00fa837a3c8c44c055eb41ae AS build

WORKDIR /app
COPY ./frontend/package*.json /app/.
RUN npm ci
EXPOSE 3000

CMD ["npm", " run start"]
