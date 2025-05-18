import { immerable } from "immer";
import { io } from "socket.io-client";

// "undefined" means the URL will be computed from the `window.location` object
const HOST_SERVER = process.env.HOST_SERVER || "localhost";
const PORT_SERVER = process.env.PORT_SERVER || 3001;
export const socket = io(`http://${HOST_SERVER}:${PORT_SERVER}`);

export default class Metrics {
  [immerable] = true;
  constructor() {
    this.epoch = [];
    this.loss = [];
    this.training_sample = null;
    this.test_sample = null;
  }
  resetState() {
    this.epoch = [];
    this.loss = [];
    this.training_sample = null;
    this.test_sample = null;
  }
  push(metrics_record) {
    const keys = Object.keys(metrics_record);
    for (let key of keys) {
      if (metrics_record[key] !== null) {
        if ((key == "epoch") & (metrics_record[key] == 1)) {
          this.resetState();
        }
        if (["epoch", "loss"].includes(key)) {
          this[key].push(metrics_record[key]);
        } else {
          this[key] = metrics_record[key];
        }
      }
    }
  }
  pull() {
    return this;
  }
}
