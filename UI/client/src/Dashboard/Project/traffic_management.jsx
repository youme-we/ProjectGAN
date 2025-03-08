import { immerable } from "immer";
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
