import React, { useEffect, useState } from "react";
import { useImmer } from "use-immer";
import { useNavigate } from "react-router-dom";
import Inputfields_project_config from "../Components/Inputfields_project_config";
import {
  create_project_config,
  read_project_config,
  update_project_config,
  delete_project_config,
} from "../traffic_management";

export default function Create_prj({ project_config, setproject_config }) {
  const navigate = useNavigate();
  useEffect(() => {
    let stored_project_config = JSON.parse(
      sessionStorage.getItem("project_config")
    );
    if (stored_project_config) {
      setproject_config(stored_project_config);
    } else {
      navigate("/home");
    }
  }, []);

  const onTune_project_config = (e, section_name, keyname) => {
    if (e.key === "Enter") {
      sessionStorage.setItem("project_config", JSON.stringify(project_config));
      document.getElementById(`inputfield_${section_name}_${keyname}`).blur();
    }
  };

  const onChange_project_config = (e, section_name, keyname) => {
    let value = e.target.value;
    if (typeof project_config[section_name][keyname] == "number") {
      value = parseFloat(value);
    }
    setproject_config((draft) => {
      draft[section_name][keyname] = value;
    });
  };

  const onClick_create_project_config = async () => {
    const res = await create_project_config(project_config);
    if (res.acknowledged) {
      sessionStorage.setItem(
        `${project_config.prj_info.name}_project_config`,
        JSON.stringify(project_config)
      );
      if (project_config.prj_info.name.trim()) {
        navigate(`/${project_config.prj_info.dashboard}`);
      }
    } else if (res.errorCode == 11000) {
      alert("Project already exists!");
    }
  };

  return (
    <div className="relative top-0 right-0 w-screen h-screen bg-white-brown">
      {project_config && (
        <div>
          <div className="flex h-full justify-evenly items-center relative top-48 bg-dark-green">
            <Inputfields_project_config
              section_name={"prj_info"}
              project_config_section={project_config.prj_info}
              onTune_project_config={onTune_project_config}
              onChange_project_config={onChange_project_config}
            />
            <Inputfields_project_config
              section_name={"trainer"}
              project_config_section={project_config.trainer}
              onTune_project_config={onTune_project_config}
              onChange_project_config={onChange_project_config}
            />
            <Inputfields_project_config
              section_name={"plot_rates"}
              project_config_section={project_config.plot_rates}
              onTune_project_config={onTune_project_config}
              onChange_project_config={onChange_project_config}
            />

            <Inputfields_project_config
              section_name={"hyperparameters"}
              project_config_section={project_config.hyperparameters}
              onTune_project_config={onTune_project_config}
              onChange_project_config={onChange_project_config}
            />
            <Inputfields_project_config
              section_name={"metadata"}
              project_config_section={project_config.metadata}
              onTune_project_config={onTune_project_config}
              onChange_project_config={onChange_project_config}
            />
            <div className="flex flex-col items-center space-y-4">
              <button
                className="px-6 py-2 bg-white-brown text-dark-green font-semibold rounded-lg shadow hover:bg-light-brown transition"
                onClick={() => onClick_create_project_config()}
              >
                Create Project
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
