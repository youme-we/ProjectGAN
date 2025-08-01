import React, { useEffect, useState } from "react";
import { useImmer } from "use-immer";
import { BrowserRouter, Route, Routes } from "react-router-dom";
import Home from "./Center/Home";
import Create_prj from "./Center/Create_prj";
import DashboardGAN from "./Dashboards/DashboardGAN/Main";
import { Navigate } from "react-router-dom";
export default function App() {
  const [overview, setoverview] = useImmer(null);
  return (
    <BrowserRouter>
      <Routes>
        <Route
          path="/home"
          element={<Home overview={overview} setoverview={setoverview} />}
        />
        <Route
          path="/create_prj"
          element={<Create_prj overview={overview} setoverview={setoverview} />}
        />
        <Route
          path="/DashboardGAN"
          element={
            <DashboardGAN overview={overview} setoverview={setoverview} />
          }
        />
      </Routes>
    </BrowserRouter>
  );
}
