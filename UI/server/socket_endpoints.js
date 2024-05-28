import http from "http";
import { Server } from "socket.io";
import express from "express";
const app = express();

const socket_endpoints = (server) => {
  const io = setup_socket_server(server);
  io.on("connection", (socket) => {
    //receive a message from the client
    socket.on("/neuronal_network_metrics_s", (data) => {
      // send data to the client
      socket.broadcast.emit("/neuronal_network_metrics_c", data);
    });

    socket.on("/play_pause_save_s", (data) => {
      socket.broadcast.emit("/play_pause_save_py", data);
      console.log(data);
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
