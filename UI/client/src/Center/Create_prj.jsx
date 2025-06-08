import React, { useEffect, useState } from "react";
import { useImmer } from "use-immer";
import { useNavigate } from "react-router-dom";
import Inputfields_overview from "../Components/Inputfields_overview";
import {
  create_prj_overview,
  read_prj_overview,
  update_prj_overview,
  delete_prj_overview,
} from "../traffic_management";

export default function Create_prj({ overview, setoverview }) {
  const navigate = useNavigate();
  useEffect(() => {
    let stored_overview = JSON.parse(sessionStorage.getItem("overview"));
    if (stored_overview) {
      setoverview(stored_overview);
    } else {
      navigate("/home");
    }
  }, []);

  const onTune_overview = (e, section_name, keyname) => {
    if (e.key === "Enter") {
      sessionStorage.setItem("overview", JSON.stringify(overview));
      document.getElementById(`inputfield_${section_name}_${keyname}`).blur();
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

  const onClick_create_prj_overview = async () => {
    const res = await create_prj_overview(overview);
    if (res.acknowledged) {
      sessionStorage.setItem(
        `${overview.prj_info.name}_overview`,
        JSON.stringify(overview)
      );
      if (overview.prj_info.name.trim()) {
        navigate(`/${overview.prj_info.dashboard}`);
      }
    } else if (res.errorCode == 11000) {
      alert("Project already exists!");
    }
  };

  return (
    <div className="relative top-0 right-0 w-screen h-screen bg-white-brown">
      {overview && (
        <div>
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
              section_name={"hyperparameters"}
              overview_section={overview.hyperparameters}
              onTune_overview={onTune_overview}
              onChange_overview={onChange_overview}
            />
            <Inputfields_overview
              section_name={"metadata"}
              overview_section={overview.metadata}
              onTune_overview={onTune_overview}
              onChange_overview={onChange_overview}
            />
            <div className="flex flex-col items-center space-y-4">
              <button
                className="px-6 py-2 bg-white-brown text-dark-green font-semibold rounded-lg shadow hover:bg-light-brown transition"
                onClick={() => onClick_create_prj_overview()}
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
