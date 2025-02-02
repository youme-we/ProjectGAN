import { Server } from "socket.io";

const socket_endpoints = (server, metrics) => {
  const io = setup_socket_server(server);
  io.on("connection", (socket) => {
    socket.on("/nn_metrics_s", (metrics_record) => {
      metrics.push(metrics_record);
      socket.broadcast.emit("/nn_metrics_c", metrics_record);
    });

    socket.on("/tune_s", (data) => {
      socket.broadcast.emit("/tune_nn", data);
    });

    socket.on("/pps_s", (data) => {
      socket.broadcast.emit("/pps_nn", data);
    });
  });
};

const setup_socket_server = (server) => {
  return new Server(server, {
    cors: {
      origin: "*",
      methods: ["GET", "POST"],
    },
  });
};

export default socket_endpoints;
