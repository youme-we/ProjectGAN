import React, { useEffect, useState } from "react";
import ReactEcharts from "echarts-for-react";

export default function Chart_EL({ metrics }) {
//sessionStorage.setItem("metrics.epoch", JSON.stringify(metrics.Chart_EL.epoch))
  console.log(metrics)
  const option = {
    xAxis: {
      type: "category",
      data: metrics.Chart_EL.epoch,
      axisLine: {
        lineStyle: {
          color: "F5F9E9"
        },
      },
      axisLabel: { color: "#F5F9E9" },
    },
    yAxis: {
      type: "value",
      axisLine: {
        lineStyle: {
          color: "#F5F9E9"
        },
      },
      axisLabel: { color: "#F5F9E9" },
    },
    series: [
      {
        data: metrics.Chart_EL.loss,
        type: "line",
        smooth: true,
        lineStyle: { color: "#F5F9E9" },
        showSymbol: false
      },
    ],
  };
  return (
    <ReactEcharts option={option} className="basis-2/3" style={{height:"400px"}}  />
  )
}

