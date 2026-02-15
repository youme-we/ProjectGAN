import React, { useEffect, useState } from "react";
import { useImmer } from "use-immer";
import { useNavigate } from "react-router-dom";
import Controllers_pps from "../../Components/Controllers_pps";
import Inputfields_project_config from "../../Components/Inputfields_project_config";
import Chart_EL from "../../Components/Chart_EL";
import SamplesTT from "../../Components/SamplesTT";
import Network from "../../Components/Network";
import {
  create_project_config,
  read_project_config,
  update_project_config,
  delete_project_config,
} from "../../traffic_management";
import { Metrics, socket } from "../../traffic_management";
import { set, update } from "lodash";

export default function DashboardGAN({ project_config, setproject_config }) {
  const navigate = useNavigate();
  const [metrics, setmetrics] = useImmer(new Metrics());
  useEffect(() => {
    socket.on("/nn_metrics_c", (metrics_record) => {
      setmetrics((draft) => {
        draft.push(metrics_record);
      });
    });
    let stored_project_config = JSON.parse(
      sessionStorage.getItem("project_config")
    );
    if (stored_project_config) {
      setproject_config(stored_project_config);
    } else {
      navigate(`/home`);
    }
    return () => {
      socket.off("/nn_metrics_c");
    };
  }, []);

  const onTune_project_config = (e, section_name, keyname) => {
    if (e.key === "Enter") {
      document.getElementById(`inputfield_${section_name}_${keyname}`).blur();
      socket.emit("/tune_s", {
        project_config: JSON.stringify(project_config),
      });
      sessionStorage.setItem("project_config", JSON.stringify(project_config));
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

  return (
    <div className="relative top-0 right-0 w-screen h-screen bg-white-brown">
      {project_config && (
        <>
          <div className="w-full px-8 py-6 border-b border-gray-800 flex items-center justify-between bg-gray-950">
            <h1 className="text-3xl font-bold text-white tracking-tight">
              ProjectGAN
            </h1>
            <div>
              {
                //TODO:Move button to Components folder
              }
              <button
                className="flex items-center m-4 gap-2 px-4 py-2 rounded-xl bg-white-brown text-dark-gray font-medium shadow hover:shadow-lg hover:bg-white transition duration-200"
                onClick={() =>
                  update_project_config(
                    project_config.prj_info.name,
                    project_config
                  )
                }
              >
                <svg
                  xmlns="http://www.w3.org/2000/svg"
                  className="h-5 w-5"
                  fill="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path
                    d="M17 3H5c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2V7l-4-4zM12 19c-1.1 0-2-.9-2-2s.9-2 
             2-2 2 .9 2 2-.9 2-2 2zm2-10H6V5h8v4z"
                  />
                </svg>
                Save project_config
              </button>
              <Controllers_pps socket={socket} />
            </div>
          </div>
          <div>
            <div className="flex h-full justify-evenly items-center relative top-48 bg-dark-green">
              <div className="font-serif text-white-brown bg-dark-gray p-6 rounded-2xl shadow-md w-fit">
                <div className="text-xl mb-2">
                  Epoch:{" "}
                  <span className="font-bold">{metrics.epoch.at(-1)}</span>
                </div>
                <div className="text-xl">
                  Loss:{" "}
                  <span className="font-bold">
                    {metrics.loss.at(-1)?.toFixed(4)}
                  </span>
                </div>
              </div>

              <Chart_EL epoch={metrics.epoch} loss={metrics.loss} />
              <Inputfields_project_config
                project_config={project_config}
                setproject_config={setproject_config}
              />
            </div>
            <SamplesTT
              training_samples={metrics.training_samples}
              test_samples={metrics.test_samples}
            />
            {/*<Network weights={metrics.weights} />*/}
            <div className="flex h-full justify-evenly items-center relative top-48 bg-dark-green"></div>
          </div>
        </>
      )}
    </div>
  );
}
