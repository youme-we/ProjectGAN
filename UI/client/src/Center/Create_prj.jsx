import React, { useEffect, useState } from "react";
import { useImmer } from "use-immer";
import { socket } from "../traffic_management";
import overview_template from "../overview_template.json";
import Inputfields_Hyperparameters from "../Components/Inputfields_Hyperparameters";
const HOST_SERVER = process.env.HOST_SERVER || "localhost";
const PORT_SERVER = process.env.PORT_SERVER || 3001;
export default function Project() {
  const [overview, setoverview] = useImmer();
  let stored_overview = JSON.parse(sessionStorage.getItem("overview"));
  console.log("hello world");
  if (stored_overview) {
    console.log("using sessionStorage");
    setoverview(stored_overview);
  } else {
    fetch(`http://${HOST_SERVER}:${PORT_SERVER}/get_prj_overview`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ prj_name: "prj_template" }),
      mode: "cors",
      credentials: "include",
    }).then((res) => console.log(res.json()));
  }
  return (
    <div className="relative top-0 right-0 w-screen h-screen bg-white-brown">
      <div>
        <div className="flex h-full justify-evenly items-center relative top-48 bg-dark-green">
          <Inputfields_Hyperparameters
            erparameters
            overview={overview}
            setoverview={setoverview}
            overview_template={overview_template}
            socket={socket}
          />
        </div>
      </div>
      )
    </div>
  );
}
