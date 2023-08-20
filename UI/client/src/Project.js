import React, {useEffect, useState} from 'react'
import {useNavigate} from "react-router-dom"

function Project() {
  const [backendData, setBackendData] = useState([{}])
  const [UsrInputValue, setUsrInputValue] = useState("")
  const [PassInputValue, setPassInputValue] = useState("")
  const navigate = useNavigate();
  


  const Send = () =>{
    fetch('http://localhost:3001/project', {
      method:"POST",
      headers: { 'Content-Type': 'application/json'},
      body: JSON.stringify({ usr:UsrInputValue,pass:PassInputValue })
    })
      .then(response => response.json())
      .then(res => {if(res){
        navigate('/auth')
      }})
       }



  return (
    <div className="Project">
      <h1>Project</h1>
      <input type={"text"} value={UsrInputValue} onChange={(e) => setUsrInputValue(e.target.value)}/>
      <input type={"password"} value={PassInputValue} onChange={(e) => setPassInputValue(e.target.value)}/>
      <button onClick={Send}>whatever</button>
    </div>  
  );
}

export default Project;


