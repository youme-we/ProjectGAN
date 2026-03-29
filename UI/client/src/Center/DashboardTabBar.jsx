import { useState } from "react";

export default function DashbaordTabBar({ tab, setTab }) {
  return (
    <div className="sticky top-0 h-12 flex flex-row  justify-center backdrop-blur-md backdrop-opacity-60 rounded-b-xs shadow-2xs/2.5  ">
      <button className="w-80" onClick={() => setTab("plots")}>
        <p className="font-sans text-xl antialiased font-semibold hover:text-2xl active:text-xl">Plots</p>
      </button>
      <button className="w-80" onClick={() => setTab("configurations")}>
        <p className="font-sans text-xl antialiased font-semibold hover:text-2xl active:text-xl">Configurations</p>
      </button>
      {/*<button class="w-80" type="button">
        Project Settings
      </button>*/}
    </div>
  );
}
