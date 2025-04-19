import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { socket } from "./sub_functions/socket";
const PORT = process.env.PORT || 3001;

export default function Create() {
  const [prj_name, setprj_name] = useState("");
  const navigate = useNavigate();

  const send = () => {
    fetch(`http://localhost:${PORT}/create`, {
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
          alert("Project already exists");
        }
      });
  };

  return (
    <div className="App">
      <h3>enter a Project_ID to create a new Project</h3>
      <input
        type={"text"}
        value={prj_name}
        onChange={(e) => setprj_name(e.target.value)}
      ></input>
      <button onClick={send}>create</button>
    </div>
  );
}
