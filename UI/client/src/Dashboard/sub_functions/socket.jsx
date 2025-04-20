import { io } from "socket.io-client";

// "undefined" means the URL will be computed from the `window.location` object
const PORT_SERVER = process.env.PORT_SERVER || 3001;
const HOST_SERVER = process.env.HOST_SERVER || "localhost";

export const socket = io(`http://${HOST_SERVER}:${PORT_SERVER}`);
