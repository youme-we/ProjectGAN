import http from "http";
import DB from "./database.js";
import socket_endpoints from "./socket_endpoints.js";
import setup_express from "./express_setup.js";
import http_endpoints from "./http_endpoints.js";
import Metrics from "./traffic_management.js";
const app = setup_express();
const server = http.createServer(app);
let db = new DB("ProjectGAN", "configs");
let metrics = new Metrics();
http_endpoints(app, db);
socket_endpoints(server, metrics);

const PORT_SERVER = process.env.PORT_SERVER || 3001;
server.listen(PORT_SERVER, "0.0.0.0", () => {
  console.log("server is listening on PORT_SERVER:", PORT_SERVER);
});
