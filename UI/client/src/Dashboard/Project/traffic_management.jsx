import { immerable } from "immer";
export default class Metrics {
  [immerable] = true;
  constructor() {
    this.epoch = [];
    this.loss = [];
    this.training_sample = null;
    this.test_sample = null;
    this.weights = null;
  }
  push(metrics_record) {
    const keys = Object.keys(metrics_record);
    for (let key of keys) {
      if (metrics_record[key] !== null) {
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
