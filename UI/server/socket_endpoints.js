import http from "http";
import { Server } from "socket.io";
import express from "express";
const app = express();

const socket_endpoints = (server) => {
  const io = setup_socket_server(server);
  io.on("connection", (socket) => {
    //receive a message from the client
    socket.on("/nn_metrics_s", (data) => {
      // send data to the client
      socket.broadcast.emit("/nn_metrics_c", data);
    });

    socket.on("/tune_s", (data) => {
      console.log("data was braodcasted")
      socket.broadcast.emit("/tune_nn", data)
    })

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
