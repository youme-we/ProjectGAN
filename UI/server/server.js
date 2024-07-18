import http from 'http'
import DB from './database.js';
import socket_endpoints from './socket_endpoints.js';
import setup_express from './express_setup.js';
import http_endpoints from './http_endpoints.js'
const PORT = 3001;
const app = setup_express();

const server = http.createServer(app);
server.listen(PORT, () => {
  console.log("socket is listening on PORT:", PORT);
});

let db = new DB("ProjectGAN", "Projects");
http_endpoints(app, db);
socket_endpoints(server);
