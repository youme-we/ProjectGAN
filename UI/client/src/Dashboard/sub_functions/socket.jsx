import { io } from "socket.io-client";

// "undefined" means the URL will be computed from the `window.location` object
const PORT = process.env.PORT || 3001;

export const socket = io(`http://localhost:${PORT}`);
