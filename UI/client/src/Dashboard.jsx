import DashbaordTabBar from "./DashboardTabBar";
import PlotsTab from "./PlotsTab";
import { useEffect, useState } from "react";

export default function Dashbaord(project_config, setproject_config) {
  const [tab, setTab] = useState("plots");

  return (
    <div className="min-h-screen w-full bg-white relative ">
      <div
        className="absolute inset-0 z-0 "
        style={{
          background: "#ffffff",
          backgroundImage: "radial-gradient(circle at 1px 1px, rgba(0, 0, 0, 0.35) 1px, transparent 0)",
          backgroundSize: "20px 20px",
        }}
      />
      <DashboardTabBar tab={tab} setTab={setTab} />
      {tab === "plots" && <PlotsTab />}
      {tab === "configurations" && <div className="relative">Configurations</div>}
      <div className="h-[300vh] flex items-start justify-center pt-20">
        <p className="text-gray-400 text-sm">scroll test — if you can scroll, it works ✓</p>
      </div>
    </div>
  );
}
