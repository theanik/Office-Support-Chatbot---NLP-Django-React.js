FROM node:18-alpine

ENV NODE_ENV development
# Add a work directory
WORKDIR /app
# Cache and Install dependencies

COPY package.json .
RUN npm install
# RUN yarn install
COPY . .
EXPOSE 5173
CMD [ "npm", "run", "dev" ]