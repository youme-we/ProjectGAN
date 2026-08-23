import { useEffect, useState } from "react";
import { useImmer } from "use-immer";
import Chart_EL from "../Plotters/Chart_EL";
import SamplesTT from "../Plotters/SamplesTT";
import { Metrics, socket } from "../traffic_management";

export default function Dashbaord(project_config, setproject_config) {
  const [tab, setTab] = useState("plots");

  return (
    <div className="relative h-screen snap-y snap-mandatory overflow-y-scroll scroll-smooth">
      <div className="sticky z-10 top-0 h-12 flex flex-row  justify-center backdrop-blur-xl backdrop-opacity-60 rounded-b-xs shadow-2xs/2.5">
        <button className="w-80" onClick={() => setTab("plots")}>
          <p className="font-sans text-xl antialiased font-semibold hover:text-2xl active:text-xl">Plots</p>
        </button>
        <button className="w-80" onClick={() => setTab("configurations")}>
          <p className="font-sans text-xl antialiased font-semibold hover:text-2xl active:text-xl">Configurations</p>
        </button>
        <button className="w-80" onClick={() => setTab("settings")}>
          <p className="font-sans text-xl antialiased font-semibold hover:text-2xl active:text-xl">Settings</p>
        </button>
      </div>
      <div hidden={tab !== "plots"}>
        <div
          className="inset-0 z-0"
          style={{
            background: "#ffffff",
            backgroundImage: "radial-gradient(circle at 1px 1px, rgba(0, 0, 0, 0.35) 1px, transparent 0)",
            backgroundSize: "20px 20px",
          }}
        >
          <PlotsTab />
        </div>
      </div>
      <div className="relative" hidden={tab !== "configurations"}>
        Configurations
      </div>
    </div>
  );
}

function PlotsTab() {
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
    <div className="relative ">
      <section className="relative h-screen snap-start bottom-[6px]">
        <Chart_EL epoch={metrics.epoch} loss={metrics.loss} className="bottom-[300px]" />
      </section>
      <section className="h-screen snap-start">
        <SamplesTT training_samples={metrics.training_samples} test_samples={metrics.test_samples} />
      </section>
      <section className="h-screen snap-start">
        <SamplesTT training_samples={metrics.training_samples} test_samples={metrics.test_samples} />
      </section>
    </div>
  );
}
