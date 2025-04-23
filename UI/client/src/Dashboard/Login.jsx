import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { socket } from "./sub_functions/socket";
const PORT_SERVER = process.env.PORT_SERVER || 3001;
const HOST_SERVER = process.env.HOST_SERVER || "localhost";

export default function Login() {
  const [prj_name, setprj_name] = useState("");
  const navigate = useNavigate();

  const send = () => {
    fetch(`http://${HOST_SERVER}:${PORT_SERVER}/login`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ prj_name }),
      mode: "cors",
      credentials: "include",
    })
      .then((res) => res.json())
      .then((res) => {
        if (res) {
          navigate("/project");
          socket.emit("/tune_s", {
            overview: JSON.stringify(res),
          });
          sessionStorage.setItem("overview", JSON.stringify(res));
        } else {
          alert("Project doesn't exist");
        }
      });
  };

  return (
    <div className="App">
      <h3>enter Project_ID</h3>
      <input
        type={"text"}
        value={prj_name}
        onChange={(e) => setprj_name(e.target.value)}
      ></input>
      <button onClick={send}>login</button>
    </div>
  );
}
