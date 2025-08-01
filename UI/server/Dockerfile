FROM node:23

WORKDIR /app

COPY package*.json ./

RUN npm install

COPY . .

ENV PORT_SERVER=3001

EXPOSE 3001

CMD ["npx", "nodemon", "server.js"]

