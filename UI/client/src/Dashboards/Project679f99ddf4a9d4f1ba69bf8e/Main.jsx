import React, { useEffect, useState } from "react";
import { useImmer } from "use-immer";
import { socket } from "../sub_functions/socket";
import overview_template from "./overview_template.json";
import Controllers_pps from "./Controllers_pps";
import Inputfields_Hyperparameters from "./Inputfields_Hyperparameters";
import Chart_EL from "./Chart_EL";
import SamplesTT from "./SamplesTT";
import Network from "./Network";
import Metrics from "./traffic_management";

export default function Project() {
  const [overview, setoverview] = useImmer(
    JSON.parse(sessionStorage.getItem("overview"))
  );
  const [metrics, setmetrics] = useImmer(new Metrics());
  useEffect(() => {
    socket.on("/nn_metrics_c", (metrics_record) => {
      setmetrics((draft) => {
        draft.push(metrics_record);
      });
    });
    return () => {
      socket.off("/nn_metrics_c");
    };
  }, []);

  return (
    <div className="relative top-0 right-0 w-screen h-screen bg-white-brown">
      <Controllers_pps socket={socket} />
      <div>
        <div className="flex h-full justify-evenly items-center relative top-48 bg-dark-green">
          <div className="font-serif text-3xl subpixel-antialiased bg-dark-gray text-white-brown">
            {metrics.epoch.at(-1)}
          </div>
          <Chart_EL epoch={metrics.epoch} loss={metrics.loss} />
          <Inputfields_Hyperparameters
            erparameters
            overview={overview}
            setoverview={setoverview}
            overview_template={overview_template}
            socket={socket}
          />
        </div>
        <SamplesTT
          training_sample={metrics.training_sample}
          test_sample={metrics.test_sample}
        />
        {/*<Network weights={metrics.weights} />*/}
      </div>
      )
    </div>
  );
}
