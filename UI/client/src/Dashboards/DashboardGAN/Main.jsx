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
            <button
              className="fill-dark-gray"
              onClick={() =>
                update_prj_overview(overview.prj_info.name, overview)
              }
            >
              Save overview
            </button>
            <Controllers_pps socket={socket} />
          </div>
          <div>
            <div className="flex h-full justify-evenly items-center relative top-48 bg-dark-green">
              <div className="font-serif text-3xl subpixel-antialiased bg-dark-gray text-white-brown">
                {metrics.epoch.at(-1)}
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
          </div>
        </>
      )}
    </div>
  );
}
