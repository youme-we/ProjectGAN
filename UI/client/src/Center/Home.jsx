import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import {
  create_project_config,
  read_project_config,
  update_project_config,
  delete_project_config,
} from "../traffic_management";
function Home({ project_config, setproject_config }) {
  const navigate = useNavigate();
  const [prj_name, setprj_name] = useState("");
  const onClick_create_prj = () => {
    read_project_config("template").then((project_config_template) => {
      setproject_config(project_config_template);
      sessionStorage.setItem(
        "project_config",
        JSON.stringify(project_config_template)
      );
      navigate("/create_prj");
    });
  };

  const onClick_open_prj = () => {
    read_project_config(prj_name).then((project_config_prj) => {
      if (project_config_prj) {
        setproject_config(project_config_prj);
        sessionStorage.setItem(
          "project_config",
          JSON.stringify(project_config_prj)
        );
        navigate(`/${project_config_prj.prj_info.dashboard}`);
      } else {
        alert("The requested project doesn't exist or is unavailable");
      }
    });
  };
  return (
    <div className="min-h-screen bg-white-brown flex items-center justify-center px-4">
      <div className="bg-white rounded-3xl shadow-xl p-10 max-w-md w-full text-center">
        <h1 className="text-4xl font-extrabold text-dark-green mb-3">
          Welcome to Project Central
        </h1>
        <p className="text-blue-gray mb-8 text-sm">
          Create and manage your projects with ease.
        </p>

        {/* Create Project Button */}
        <button
          onClick={() => onClick_create_prj()}
          className="bg-dark-green hover:bg-blue-gray text-white font-semibold py-3 px-6 rounded-xl shadow-md transition-all w-full mb-6"
        >
          Create New Project
        </button>

        {/* Divider */}
        <div className="flex items-center justify-center my-6">
          <span className="border-t border-light-brown w-full"></span>
          <span className="px-3 text-sm text-light-brown font-medium">or</span>
          <span className="border-t border-light-brown w-full"></span>
        </div>

        {/* Project ID input and button */}
        <input
          type="text"
          placeholder="Enter project ID or name"
          value={prj_name}
          onChange={(e) => setprj_name(e.target.value)}
          className="border border-light-brown rounded-xl px-4 py-2 mb-4 w-full text-sm text-dark-gray focus:outline-none focus:ring-2 focus:ring-dark-green"
        />
        <button
          onClick={() => onClick_open_prj()}
          className="bg-light-brown hover:bg-dark-gray text-white font-medium py-2 px-6 rounded-xl w-full transition-all"
        >
          Open Project
        </button>
      </div>
    </div>
  );
}

export default Home;
