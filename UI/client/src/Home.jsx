import React, {useEffect, useState} from 'react'
import {useNavigate} from "react-router-dom"

function Home() {
  const navigate = useNavigate();
  return (
    <div className="Home">
      <button onClick={()=>navigate('/create')}>create</button>
      <button onClick={()=>navigate('/login')}>login</button>
    </div>  
  );
}

export default Home;


