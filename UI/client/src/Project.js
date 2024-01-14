import React, { useEffect, useState } from "react";
import { socket } from "./socket";
import ReactEcharts from "echarts-for-react";
import PlayArrowIcon from "@mui/icons-material/PlayArrow";
import PlayDisabledIcon from "@mui/icons-material/PlayDisabled";
import PauseIcon from "@mui/icons-material/Pause";
import Network from "./Network.js"

function Project() {
  const [data, setdata] = useState([]);
  const [show, setshow] = useState(false);
  socket.on("/send_c", (data) => {
    setdata(data);
    setshow(true)
  });

  const play_stop = (pause, save, run) => {
    socket.emit("/play_pause_save_s", {
      pause: pause,
      save: save,
      run: run

    });
  };

  // Draw the chart
  const option = {
    xAxis: {
      type: "category",
      data: data.epoch,
    },
    yAxis: {
      type: "value",
    },
    series: [
      {
        data: data.loss,
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
          onClick={() => play_stop(false, false, true)}
          style={ButtonStyle}
        />
        <PauseIcon
          onClick={() => play_stop(true, false, true)}
          style={ButtonStyle}
        />
        <PlayDisabledIcon
          onClick={() => play_stop(false, true, false)}
          style={ButtonStyle}
        />
      </div>
      <ReactEcharts option={option} />
      <img
        style={{ width: "400px", height: "auto" }}
        src={`data:image/png;base64,${data.generated_data}`}
      />
      <img
        style={{ width: "400px", height: "auto" }}
        src={`data:image/png;base64,${data.imitated_data}`}
      />
    {show === true &&
    <Network weights = {data.weights}/>
    }
    </div>
  );
}

export default Project;
