import React, { useEffect, useState } from "react";
import { socket } from "./socket";
import ReactEcharts from "echarts-for-react";

function Project() {
  const [data, setdata] = useState([]);
  var imgChunks = [];
  socket.on("/send_c", (data) => {
    setdata(data);
  });

  console.log(data);
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
  return (
    <div className="Project">
      <ReactEcharts option={option} />
      <img
        style={{ width: "400px", height:'auto' }}
        src={`data:image/png;base64,${data.generated_data}`}
      />
      <img
        style={{ width: "400px", height:'auto' }}
        src={`data:image/png;base64,${data.imitated_data}`}
      />
    </div>
  );
}

export default Project;
