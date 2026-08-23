import { useEffect, useState } from "react";
import { useImmer } from "use-immer";
import Chart_EL from "../Components/Chart_EL";
import { Metrics, socket } from "../traffic_management";
export default function PlotsTab() {
  const [metrics, setMetrics] = useImmer(new Metrics());
  useEffect(() => {
    socket.on("nn_metrics_c", (metrics_record) => {
      setMetrics((draft) => {
        draft.push(metrics_record);
      });
    });
    return () => {
      socket.off("nn_metrics_c");
    };
  }, []);

  return (
    <div>
      <Chart_EL epoch={metrics.epoch} loss={metrics.loss} />
    </div>
  );
}
