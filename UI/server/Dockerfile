FROM node:23

WORKDIR /app

COPY package*.json ./

RUN npm install

COPY . .

ENV DB_HOST="host.docker.internal"
ENV PORT=3001

EXPOSE 3001

CMD ["npx", "nodemon", "server.js"]

