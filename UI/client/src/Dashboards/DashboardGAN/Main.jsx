import React, { useEffect, useState } from "react";
import { useImmer } from "use-immer";
import { useNavigate } from "react-router-dom";
import Controllers_pps from "../../Components/Controllers_pps";
import Inputfields_overview from "../../Components/Inputfields_overview";
import Chart_EL from "../../Components/Chart_EL";
import SamplesTT from "../../Components/SamplesTT";
import Network from "../../Components/Network";
import {
  create_prj_overview,
  read_prj_overview,
  update_prj_overview,
  delete_prj_overview,
} from "../../traffic_management";
import { Metrics, socket } from "../../traffic_management";
import { update } from "lodash";

export default function DashboardGAN({ overview, setoverview }) {
  const navigate = useNavigate();
  const [metrics, setmetrics] = useImmer(new Metrics());
  useEffect(() => {
    socket.on("/nn_metrics_c", (metrics_record) => {
      setmetrics((draft) => {
        draft.push(metrics_record);
      });
    });
    let stored_overview = JSON.parse(sessionStorage.getItem("overview"));
    if (stored_overview) {
      setoverview(stored_overview);
    } else {
      navigate(`/home`);
    }
    return () => {
      socket.off("/nn_metrics_c");
    };
  }, []);

  const onTune_overview = (e, section_name, keyname) => {
    if (e.key === "Enter") {
      document.getElementById(`inputfield_${section_name}_${keyname}`).blur();
      socket.emit("/tune_s", {
        overview: JSON.stringify(overview),
      });
      sessionStorage.setItem("overview", JSON.stringify(overview));
    }
  };

  const onChange_overview = (e, section_name, keyname) => {
    let value = e.target.value;
    if (typeof overview[section_name][keyname] == "number") {
      value = parseFloat(value);
    }
    setoverview((draft) => {
      draft[section_name][keyname] = value;
    });
  };

  return (
    <div className="relative top-0 right-0 w-screen h-screen bg-white-brown">
      {overview && (
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
                  update_prj_overview(overview.prj_info.name, overview)
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
                Save Overview
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
              <Inputfields_overview
                section_name={"hyperparameters"}
                overview_section={overview.hyperparameters}
                onTune_overview={onTune_overview}
                onChange_overview={onChange_overview}
              />
            </div>
            <SamplesTT
              training_samples={metrics.training_samples}
              test_samples={metrics.test_samples}
            />
            {/*<Network weights={metrics.weights} />*/}
            <div className="flex h-full justify-evenly items-center relative top-48 bg-dark-green">
              <Inputfields_overview
                section_name={"prj_info"}
                overview_section={overview.prj_info}
                onTune_overview={onTune_overview}
                onChange_overview={onChange_overview}
              />
              <Inputfields_overview
                section_name={"trainer"}
                overview_section={overview.trainer}
                onTune_overview={onTune_overview}
                onChange_overview={onChange_overview}
              />
              <Inputfields_overview
                section_name={"plot_rates"}
                overview_section={overview.plot_rates}
                onTune_overview={onTune_overview}
                onChange_overview={onChange_overview}
              />

              <Inputfields_overview
                section_name={"metadata"}
                overview_section={overview.metadata}
                onTune_overview={onTune_overview}
                onChange_overview={onChange_overview}
              />
            </div>
          </div>
        </>
      )}
    </div>
  );
}
