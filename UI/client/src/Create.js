import React, {useEffect, useState} from 'react'
import {useNavigate} from "react-router-dom"

function Create() {
  const [backendData, setBackendData] = useState([{}])
  const [IDInputValue, setIDInputValue] = useState("")
  const navigate = useNavigate();
  


  const Send = () =>{
    fetch('http://localhost:3001/create', {
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
        else{alert('ID exists already')}
      }) 
  }



  return (
    <div className="App">
      <h3>enter a Project_ID to create new Project</h3>
      <input type={"text"} value={IDInputValue} onChange={(e) => setIDInputValue(e.target.value)}></input>
      <button onClick={Send}>create</button>
    </div>  
  );
}

export default Create;


