import React, { useEffect, useState } from "react";
import { useImmer } from "use-immer";
import { socket } from "../sub_functions/socket.jsx";
import ReactEcharts from "echarts-for-react";
import PlayArrowIcon from "@mui/icons-material/PlayArrow";
import PlayDisabledIcon from "@mui/icons-material/PlayDisabled";
import PauseIcon from "@mui/icons-material/Pause";
import overview_template from "./overview_template.json"
import Network from "./Network.jsx";


export default function Project() {
  const [overview, setoverview] = useImmer(JSON.parse(sessionStorage.getItem('overview')))
  const [metrics, setmetrics] = useState([]);

  socket.on("/nn_metrics_c", (metrics) => {
    setmetrics(metrics);
  });

  const pps = (pause, save, run) => {
    socket.emit("/pps_s", {
      pause: pause,
      save: save,
      run: run
    })
  };


  const onTune_overview = (e) => {
    if (e.key === "Enter") {
      sessionStorage.setItem("overview", JSON.stringify(overview))
      socket.emit("/tune_s", {
        overview: JSON.stringify({ overview })
      })
    }
  }


  const onChange_overview = (e, keyname) => {
    setoverview((draft) => {
      draft.hyperparameters[keyname] = parseFloat(e.target.value)
    })
  }



  // Draw the chart
  const option = {
    xAxis: {
      type: "category",
      data: metrics.epoch,
    },
    yAxis: {
      type: "value",
    },
    series: [
      {
        data: metrics.loss,
        type: "line",
        smooth: true,
      },
    ],
  };

  const ButtonStyle = {
    width: "30px",
    height: "auto",
    color: "black",
  };
  return (
    <div className="Project">
      <div style={{ border: "2px solid", borderRadius: "5px", width: "100px" }}>
        <PlayArrowIcon
          onClick={() => pps(false, false, true)}
          style={ButtonStyle}
        />
        <PauseIcon
          onClick={() => pps(true, false, true)}
          style={ButtonStyle}
        />
        <PlayDisabledIcon
          onClick={() => pps(false, true, false)}
          style={ButtonStyle}
        />
      </div>
      {Object.keys(overview.hyperparameters).map((keyname, index) => (
        <div key={index} >
          <div>{keyname}</div>
          <input type={overview_template.hyperparameters[keyname].type}
            min={overview_template.hyperparameters[keyname].min}
            max={overview_template.hyperparameters[keyname].max}
            step={overview_template.hyperparameters[keyname].step}
            value={overview.hyperparameters[keyname]}
            onChange={(e) => { onChange_overview(e, keyname) }}
          //onKeyDown={(e) => { onTune_overview(e) }}
          />
        </div>)
      )}


      {metrics.epoch &&
        <>
          <ReactEcharts option={option} />
          <img
            style={{ width: "400px", height: "auto" }}
            src={`data:image/png;base64,${metrics.training_sample}`}
          />
          <img
            style={{ width: "400px", height: "auto" }}
            src={`data:image/png;base64,${metrics.test_sample}`}
          />
          <Network weights={metrics.weights} />
        </>
      }
    </div>
  );
}

