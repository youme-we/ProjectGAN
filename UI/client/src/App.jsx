import React, { useEffect, useState } from "react";
import { useImmer } from "use-immer";
import { BrowserRouter, Route, Routes } from "react-router-dom";
import Home from "./Center/Home";
import Create_prj from "./Center/Create_prj";
import DashboardGAN from "./Dashboards/DashboardGAN/Main";
import { Navigate } from "react-router-dom";
export default function App() {
  const [project_config, setproject_config] = useImmer(null);
  return (
    <BrowserRouter>
      <Routes>
        <Route
          path="/home"
          element={
            <Home
              project_config={project_config}
              setproject_config={setproject_config}
            />
          }
        />
        <Route
          path="/create_prj"
          element={
            <Create_prj
              project_config={project_config}
              setproject_config={setproject_config}
            />
          }
        />
        <Route
          path="/DashboardGAN"
          element={
            <DashboardGAN
              project_config={project_config}
              setproject_config={setproject_config}
            />
          }
        />
      </Routes>
    </BrowserRouter>
  );
}
