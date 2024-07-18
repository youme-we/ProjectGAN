import React, { useEffect, useState } from "react";
import { BrowserRouter, Route, Routes } from 'react-router-dom';
import Home from './Home';
import Create from './Create';
import Login from './Login';
import Project from './Project';


function Events() {
  const [overview, setoverview] = useState([])
  useEffect(() => {
  })
  return (
    <BrowserRouter>
      <Routes>
        <Route path='/' element={<Home />} />
        <Route path='/login' element={<Login setoverview={setoverview} />} />
        <Route path='/create' element={<Create setoverview={setoverview} />} />
        <Route path='/project' element={<Project overview={overview} setoverview={setoverview} />} />
      </Routes>
    </BrowserRouter>

  )
}

export default Events;

