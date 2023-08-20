import React, {useEffect, useState} from 'react'
import {useNavigate} from "react-router-dom"

function Login() {
  const [backendData, setBackendData] = useState([{}])
  const [IDInputValue, setIDInputValue] = useState("")
  const navigate = useNavigate();
  


  const Send = () =>{
    fetch('http://localhost:3001/login', {
      method:"POST",
      headers: { 'Content-Type': 'application/json'},
      body: JSON.stringify({ ID:IDInputValue}),
      mode:'cors',
      credentials: "include",
    })
      .then(response => response.json())
      .then(res => {if(res){
        navigate("/project")
      }
        else{alert('wrong Project_ID')}
      }) 
  }



  return (
    <div className="App">
      <h3>enter extisting Project_ID to enter Project</h3>
      <input type={"text"} value={IDInputValue} onChange={(e) => setIDInputValue(e.target.value)}></input>
      <button onClick={Send}>login</button>
    </div>  
  );
}

export default Login;


