import React, { useEffect, useState } from 'react'
import { useNavigate } from "react-router-dom"
import { socket } from "./socket";

function Login({setoverview}) {
  const [prj_name, setprj_name] = useState("")
  const navigate = useNavigate();



  const Send = () => {
    fetch('http://localhost:3001/login', {
      method: "POST",
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ prj_name }),
      mode: 'cors',
      credentials: "include",
    })
      .then(res => res.json())
      .then(res => {
        if (res) {
          navigate("/project")
          socket.emit("/tune_s", {
            res
          });
          setoverview(res)
        }
        else { alert("Project doesn't exist") }
      })
  }



  return (
    <div className="App">
      <h3>enter Project_ID</h3>
      <input type={"text"} value={prj_name} onChange={(e) => setprj_name(e.target.value)}></input>
      <button onClick={Send}>login</button>
    </div>
  );
}

export default Login;


