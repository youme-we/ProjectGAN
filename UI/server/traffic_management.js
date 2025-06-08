export default class Metrics {
  constructor() {
    this.epoch = [];
    this.loss = [];
    this.training_samples = null;
    this.test_samples = null;
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
}
