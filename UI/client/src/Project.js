import React, { useEffect, useState } from "react";
import { socket } from './socket';
import ReactEcharts from "echarts-for-react";

function Project() {
  const [data, setdata] = useState([])
  socket.on('/send_c', (data) => {
    setdata(data)
  });
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
      <ReactEcharts option={option} />;
    </div>
  );
}

export default Project;


