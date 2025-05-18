import React from "react";
import ReactDOM from "react-dom/client";
import reportWebVitals from "./reportWebVitals";
import { BrowserRouter, Route, Routes } from "react-router-dom";
import "./index.css";
import Home from "./Center/Home";
import Create_prj from "./Center/Create_prj";
//import Project from "./Dashboards/Project679f99ddf4a9d4f1ba69bf8e/Main";

const root = ReactDOM.createRoot(document.getElementById("root"));
root.render(
  <React.StrictMode>
    <BrowserRouter>
      <Routes>
        <Route path="/home" element={<Home />} />
        <Route path="/create_prj" element={<Create_prj />} />
        {/*
        <Route path="/dashboard" element={<Project />} />
          */}
      </Routes>
    </BrowserRouter>{" "}
  </React.StrictMode>
);

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
reportWebVitals();
