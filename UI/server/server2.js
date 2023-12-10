import express from 'express';
import cors from 'cors';
import sessions from 'express-session';
import cookieParser from 'cookie-parser';
import http from 'http'
import path from 'path';
const path_build = '/Users/skost/coding-s/ProjectGAN/UI/client/build';
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

let prjs_db_data = new DB("ProjectGAN","Projects");
http_endpoints(app, prjs_db_data);
socket_endpoints(server);
