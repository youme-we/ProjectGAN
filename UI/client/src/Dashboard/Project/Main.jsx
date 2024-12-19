import React, { useEffect, useState } from "react";
import { useImmer } from "use-immer";
import { socket } from "../sub_functions/socket";
import overview_template from "./overview_template.json"
import Controllers_pps from "./Controllers_pps"
import Inputfields_Hyperparameters from "./Inputfields_Hyperparameters"
import Chart_EL from "./Chart_EL"
import Samples_TT from "./Samples_TT"
import Network from "./Network";

export default function Project() {
  const [overview, setoverview] = useImmer(JSON.parse(sessionStorage.getItem("overview")))
  const [metrics, setmetrics] = useState([]);

  socket.on("/nn_metrics_c", (metrics) => {
    setmetrics(metrics);
  });


  return (
    <div className="relative top-0 right-0 w-screen h-screen bg-white-brown">
      <Controllers_pps socket={socket} />
      {metrics.Chart_EL &&
        <div>
          <div className="flex h-full justify-evenly items-center relative top-48 bg-dark-green">
            <Chart_EL metrics={metrics} />
            <Inputfields_Hyperparameters overview={overview} setoverview={setoverview} overview_template={overview_template} socket={socket} />
          </div>
            <Samples_TT metrics={metrics} />
            <Network weights={metrics.Network.weights} />
        </div>
      }
    </div>);
}

