import { Metrics, socket } from "../traffic_management";
export default function Inputfields_project_config({
  project_config,
  setproject_config,
}) {
  const onTune_project_config = (e, id) => {
    if (e.key === "Enter") {
      document.getElementById(id).blur();
      socket.emit("tune_s", {
        project_config: JSON.stringify(project_config),
      });
      sessionStorage.setItem("project_config", JSON.stringify(project_config));
    }
  };

  return (
    <div className="">
      <div className="heading_inputfield_project_config">Sample Size</div>
      <input
        id={`inputfield_project_config_hyperparameters_sample_size`}
        className="inputfield_project_config"
        type="number"
        value={project_config["hyperparameters"]["sample_size"]}
        onChange={(e) => {
          setproject_config((draft) => {
            draft["hyperparameters"]["sample_size"] = parseFloat(
              e.target.value
            );
          });
        }}
        onKeyDown={(e) => {
          onTune_project_config(
            e,
            "inputfield_project_config_hyperparameters_sample_size"
          );
        }}
      />
      <p></p>
      <div className="heading_inputfield_project_config">Batch Size</div>
      <input
        id={`inputfield_project_config_hyperparameters_batch_size`}
        className="inputfield_project_config"
        type="number"
        value={project_config["hyperparameters"]["batch_size"]}
        onChange={(e) => {
          setproject_config((draft) => {
            draft["hyperparameters"]["batch_size"] = parseFloat(e.target.value);
          });
        }}
        onKeyDown={(e) => {
          onTune_project_config(
            e,
            "inputfield_project_config_hyperparameters_batch_size"
          );
        }}
      />
      <p></p>
      <div className="heading_inputfield_project_config">Learning Rate</div>
      <input
        id={`inputfield_project_config_hyperparameters_learning_rate`}
        className="inputfield_project_config"
        type="number"
        value={project_config["hyperparameters"]["learning_rate"]}
        onChange={(e) => {
          setproject_config((draft) => {
            draft["hyperparameters"]["learning_rate"] = parseFloat(
              e.target.value
            );
          });
        }}
        onKeyDown={(e) => {
          onTune_project_config(
            e,
            "inputfield_project_config_hyperparameters_learning_rate"
          );
        }}
      />
      <p></p>
      <div className="heading_inputfield_project_config">Momentum</div>
      <input
        id={`inputfield_project_config_hyperparameters_momentum`}
        className="inputfield_project_config"
        type="number"
        value={project_config["hyperparameters"]["momentum"]}
        onChange={(e) => {
          setproject_config((draft) => {
            draft["hyperparameters"]["momentum"] = parseFloat(e.target.value);
          });
        }}
        onKeyDown={(e) => {
          onTune_project_config(
            e,
            "inputfield_project_config_hyperparameters_momentum"
          );
        }}
      />
      <p></p>
    </div>
  );
}
