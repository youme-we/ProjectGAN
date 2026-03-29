import { useImmer } from "use-immer";
import { BrowserRouter, Route, Routes } from "react-router-dom";
import Home from "./Center/Home";
import Dashboard from "./Center/Dashboard";
import Create_project from "./Center/Create_project";
import DashboardGAN from "./Dashboards/DashboardGAN/Main";

export default function App() {
  const [project_config, setproject_config] = useImmer(null);
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/home" element={<Home project_config={project_config} setproject_config={setproject_config} />} />
        <Route path="/create_project" element={<Create_project project_config={project_config} setproject_config={setproject_config} />} />
        <Route path="/DashboardGAN" element={<DashboardGAN project_config={project_config} setproject_config={setproject_config} />} />
        <Route path="/Dashboard" element={<Dashboard project_config={project_config} />} />
      </Routes>
    </BrowserRouter>
  );
}
