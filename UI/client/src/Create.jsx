import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { socket } from "./socket";

export default function Create({ setoverview }) {
  const [prj_name, setprj_name] = useState("")
  const navigate = useNavigate();
  const send = () => {
    fetch("http://localhost:3001/create", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ prj_name }),
      mode: "cors",
      credentials: "include",
    })
      .then(res => res.json())
      .then(res => {
        if (res) {
          navigate("/project")
          socket.emit("/tune_s", {
            overview:JSON.stringify({res})
          });
          setoverview(res)
        }
        else { alert("Project_ID already exists") }
      })
  }

  return (
    <div className="App">
      <h3>enter a Project_ID to create new Project</h3>
      <input
        type={"text"}
        value={prj_name}
        onChange={(e) => setprj_name(e.target.value)}
      ></input>
      <button onClick={send}>create</button>
    </div>

  )

}

