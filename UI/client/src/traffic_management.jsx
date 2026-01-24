import { immerable } from "immer";
import { io } from "socket.io-client";

const HOST_SERVER = process.env.REACT_APP_HOST_SERVER || "localhost";
const PORT_SERVER = process.env.REACT_APP_PORT_SERVER || 3001;
export const socket = io(`http://${HOST_SERVER}:${PORT_SERVER}`);

export async function create_project_config(project_config) {
  const res = await fetch(
    `http://${HOST_SERVER}:${PORT_SERVER}/create_project_config`,
    {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ project_config }),
      mode: "cors",
      credentials: "include",
    }
  );
  return res.json();
}
export async function read_project_config(prj_name) {
  const res = await fetch(
    `http://${HOST_SERVER}:${PORT_SERVER}/read_project_config`,
    {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ prj_name }),
      mode: "cors",
      credentials: "include",
    }
  );
  return res.json();
}
export async function update_project_config(prj_name, fields) {
  const res = await fetch(
    `http://${HOST_SERVER}:${PORT_SERVER}/update_project_config`,
    {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ prj_name, fields }),
      mode: "cors",
      credentials: "include",
    }
  );
  return res.json();
}
export async function delete_project_config(prj_name) {
  const res = await fetch(
    `http://${HOST_SERVER}:${PORT_SERVER}/delete_project_config`,
    {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ prj_name }),
      mode: "cors",
      credentials: "include",
    }
  );
  return res.json();
}
//TODO:Use functional Component for Metrics
export class Metrics {
  [immerable] = true;
  constructor() {
    this.epoch = [];
    this.loss = [];
    this.training_samples = null;
    this.test_samples = null;
  }
  resetState() {
    this.epoch = [];
    this.loss = [];
    this.training_samples = null;
    this.test_samples = null;
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
}
