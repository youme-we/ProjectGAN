import ReactEcharts from "echarts-for-react";

export default function Chart_EL({ epoch, loss }) {
  const option = {
    animationDurationUpdate: 300,
    xAxis: {
      type: "value",
      data: epoch,
      splitNumber: 4,
      axisLabel: {
        fontSize: 1,
      },
    },
    yAxis: {
      type: "value",
    },
    series: [
      {
        data: loss,
        type: "line",
        smooth: true,
      },
    ],
  };
  return (
    <div className="h-full">
      <ReactEcharts option={option} className="!h-full" />{" "}
    </div>
  );
}
