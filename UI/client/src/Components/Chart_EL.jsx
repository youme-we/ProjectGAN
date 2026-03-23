import ReactEcharts from "echarts-for-react";

export default function Chart_EL({ epoch, loss }) {
  const option = {
    xAxis: {
      type: "category",
      data: epoch,
      axisLine: {
        lineStyle: {
          color: "#000000",
        },
      },
      axisLabel: { color: "#000000" },
    },
    yAxis: {
      type: "value",
      axisLine: {
        lineStyle: {
          color: "#000000",
        },
      },
      axisLabel: { color: "#000000" },
    },
    series: [
      {
        data: loss,
        type: "line",
        smooth: true,
        smoothMonotone: "x",
        lineStyle: { color: "#000000" },
        showSymbol: false,
      },
    ],
  };
  return <ReactEcharts option={option} className="basis-2/3" style={{ height: "400px" }} />;
}
